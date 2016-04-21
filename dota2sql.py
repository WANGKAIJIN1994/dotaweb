# -*- coding: utf-8 -*-
import pymysql
import traceback
import hashlib
import types
import json
import dota2api
import threading  
import time

D2_API_KEY = '0EB71FBD16527AF680B88D79067AF1B6'

api = dota2api.Initialise(api_key=D2_API_KEY)

def md5(str):
    if type(str) is bytes:
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()
    else:
        return ''

#该函数用于将其自动转换为int并判断是否加''
def get_value_sql(val):
    if isinstance(val,int):
        return(str(val)) 
    if isinstance(val,str):
        if str.isdigit(val):
            return str(val)
    return '"%s"' % val

def get_update_sql(dic):
    sql = ''
    for k,v in dic.items():
      sql += '`' + k + '`= ' + get_value_sql(v) + ','
    return sql[:-1]

def get_insert_sql(dic):
    col = ''
    val = ''
    for k,v in dic.items():
      col += '`' + k + '`,'
      val += get_value_sql(v) + ','
    col = col[:-1]
    val = val[:-1]
    return '(' + col + ') VALUES (' + val + ');'


class Dota2SQL:
  def __init__(self,host='ali.banixc.com',user='dota',passwd='dotaer',db='dota',port=3306,charset='utf8'):
    self.host = host
    self.user = user
    self.passwd = passwd
    self.db = db
    self.port = port
    self.charset = charset
    try:
      self.conn = pymysql.connect(host,user,passwd,db,port,charset)
    except:
      traceback.print_exc()

  def __del__(self):
    try:
      self.conn.close()
    except:
      traceback.print_exc()

### 以下函数请勿调用
  def __query(self,sql):
    try:
      cur = self.conn.cursor()
      cur.execute(sql)
      data = cur.fetchall()
      cur.close()
      # print(data)
      return data         #返回结果集
    except:
      traceback.print_exc()

  def __exe(self,sql):
    try:
      cur = self.conn.cursor()
      cul= cur.execute(sql)
      self.conn.commit()
      cur.close()
      return cul          #返回受影响的行数
    except:
      traceback.print_exc()

  # def insert_item(self,dic,table):
  #   try:
  #      sql = 'DELETE FROM ' + table
  #      self.__exe(sql)
  #      for value in dic[table]:
  #       col = ''
  #       val = ''
  #       for k,v in value.items():
  #         col += '`' + k + '`,'
  #         val += '\"' + v + '\",' if isinstance(v,str) else str(v) + ','
  #       col = col[:-1]
  #       val = val[:-1]
  #       sql = 'INSERT INTO `' + table + '` (' + col + ') VALUES (' + val + ');'
  #       self.__exe(sql)
  #   except:
  #     traceback.print_exc()
  #   print('update item success!')

  def update_steam_msg(self,dic):
    steamid=int(dic['steamid'])
    sql = 'REPLACE INTO `steam` %s' % get_insert_sql(dic)
    return self.__exe(sql)
### 以上函数请勿调用

### 以下函数可供View层调用
  def login(self,username,password):
    sql = 'select `uid`,`username`,`password` from `users` where `username` = "' + username + '";'
    data = self.__query(sql)
    if not data:
      return 'USER_NOT_FIND' 
    if md5((username + password + '+5').encode('utf-8')) == data[0][2]:
      return data[0]
    return 'PASSWORD_ERROR'

  #注册时将数据提交到数据库
  def register(self,username,password,email):
    sql = 'insert into `users` (`username`,`password`,`email`) VALUES ( "'+ username +'" , "'+md5((username + password + '+5').encode('utf-8'))+'","' + email + '");'
    return self.__exe(sql)

  #注册时用于验证是否该用户名或者邮箱已经存在
  def judgeUser(self,username,email):
    sql = 'select * FROM `users` WHERE `username` = "' + username + '" ;'
    data = self.__query(sql)
    if len(data) > 0:
        return 'USERNAME_EXIST'
    sql = 'select * FROM `users` WHERE `email` = "' + email  + '";'
    data = self.__query(sql)

    if len(data) > 0:
        return 'EMAIL_EXIST'
    return 'NOTHING_EXIST'

  def get_user(self,username):
    sql = 'select * FROM `users` WHERE `username` = "' + username + '" ;'
    return self.__query(sql)

  def changepwd(self,email,password):
    sql = 'select `uid`,`username`,`password` from `users` where `email` = "' + email + '";'
    data = self.__query(sql)
    username = data[0][1]
    sql = 'update `users` set `password` = "'+ md5((username + password + '+5').encode('utf-8')) +'" where email = "'+email+'";'
    self.__exe(sql)

  def get_heroes(self):
    sql = 'SELECT * FROM `heroes`;'
    return self.__query(sql)

  def get_heroes_abilities(self):
    sql = 'SELECT * FROM `heroes_abilities`;'
    return self.__query(sql)

  def get_items(self):
    sql = 'SELECT * FROM `items`;'
    return self.__query(sql)

  def get_steamid_user(self,username):
    sql = 'select steamid FROM `users` WHERE `username` = "' + username + '" ;'
    data = self.__query(sql)
    if len(data) > 0:
      return data[0][0]
    else:
      return None

  def get_watch_list(self,uid):
    sql = 'SELECT * FROM `watchs` WHERE `uid` = %d;' % uid;
    return self.__query(sql)

  def add_watch_list(self,uid,account_id):
    sql = 'INSERT INTO `watchs` (`uid`,`account_id`) VALUES (%d,%d)' % (uid,account_id)
    return self.__exe(sql)

  def get_steam_msg(self,steamid):
    Fetch(method='get_player_summaries',steamids=steamid).start()
    sql = 'SELECT * FROM `steam` WHERE `steamid` = %s' % steamid;
    print(sql)
    data = self.__query(sql)
    # print(data)
    if len(data) > 0:
      return data[0]
    else:
      return None

  def set_steam_id(self,uid,steamid):
    self.get_steam_msg(steamid)
    sql = 'UPDATE `users` SET `steamid` = %d WHERE `uid` = %d' % (steamid,uid) 
    return self.__exe(sql)

  def set_account_id(self,uid,account_id):
      sql = 'UPDATE `users` SET `account_id` = %d WHERE `uid` = %d' % (account_id,uid) 
      return self.__exe(sql)

class Fetch(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, method, **kwargs):  
        threading.Thread.__init__(self)  
        self.method = method  
        self.kwargs = kwargs
        self.dsql = Dota2SQL()
        # self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put what you want the thread do here  
        if self.method == 'get_match_history':
            self.get_match_history()

        if self.method == 'get_player_summaries':
            self.get_player_summaries()

    def get_player_summaries(self):
        data = api.get_player_summaries(**self.kwargs)
        if len(data['players']) > 0:
            self.dsql.update_steam_msg(data['players'][0])

    def get_match_history(self):
        match = api.get_match_history(self.get_necessary_params('account_id'))
        return match




   
def test():  
    # thread1 = Fetch('heroes',1)  
    # thread2 = Fetch('items',1)  
    # thread1.start()
    # thread2.start()
    # thread3 = Fetch('get_match_details','1000193456').start()
    thread4 = Fetch(method='get_player_summaries',steamids=76561198121063498).start()
    # thread5 = Fetch('get_match_history',account_id=76482434).start()

def test2():
    dsql = Dota2SQL()
    # print(dsql.set_account_id(31,1232131123))
    # print(
    dsql.get_steam_msg(76561198299172651)
      # )

   
if __name__ == '__main__':  
    # test()
    test2()
    pass
