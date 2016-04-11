# -*- coding: utf-8 -*-
import pymysql
import traceback
import hashlib
import types


def md5(str):
    if type(str) is bytes:
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()
    else:
        return ''

class dota2sql:
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

  def query(self,sql):
    try:
      cur = self.conn.cursor()
      cur.execute(sql)
      data = cur.fetchall()
      cur.close()
      return data         #返回结果集
    except:
      traceback.print_exc()

  def exe(self,sql):
    try:
      cur = self.conn.cursor()
      cul= cur.execute(sql)
      self.conn.commit()
      cur.close()
      return cul          #返回受影响的行数
    except:
      traceback.print_exc()

  def update_item(self,dic):
    try:
       sql = 'DELETE FROM items'
       self.exe(sql)
       cur = self.conn.cursor()
       for value in dic['items']:
        col = ''
        val = ''
        for k,v in value.items():
          col += '`' + k + '`,'
          val += '\"' + v + '\",' if isinstance(v,str) else str(v) + ','
        col = col[:-1]
        val = val[:-1]
        sql = 'INSERT INTO `items` (' + col + ') VALUES (' + val + ');'
        cul = self.exe(sql)
    except:
      traceback.print_exc()
    print('update item success!')

  def login(self,username,password):
    sql = 'select `uid`,`username`,`password` from `users` where `username` = "' + username + '";'
    data = self.query(sql)
    if not data:
      return 'USER_NOT_FIND' 
    if md5((username + password + '+5').encode('utf-8')) == data[0][2]:
      return data[0]
    return 'PASSWORD_ERROR'

  def register(self,username,password):
    sql = 'insert into `users` (`username`,`password`) VALUES ( "'+ username +'" , "'+md5((username + password + '+5').encode('utf-8'))+'");'
    return self.exe(sql)

