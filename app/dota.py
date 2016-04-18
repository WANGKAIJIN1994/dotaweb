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

  def sqlexe(self,sql):
    try:
      cur = self.conn.cursor()
      cur.execute(sql)
      data = cur.fetchall()
      cur.close()
      return data
    except:
      traceback.print_exc()


    #闫正阳，这个函数不能运行成功，
    #因为我没有更改sqlexe函数为exe，
    #我在views.py中使用过sqlexe函数
    #如果在这里更改函数名会导致我view.py这种更改很多，
    #所以这个函数不会运行成功
  def insert_item(self,dic,table):
    try:
       sql = 'DELETE FROM ' + table
       self.exe(sql)
       for value in dic[table]:
        col = ''
        val = ''
        for k,v in value.items():
          col += '`' + k + '`,'
          val += '\"' + v + '\",' if isinstance(v,str) else str(v) + ','
        col = col[:-1]
        val = val[:-1]
        sql = 'INSERT INTO `' + table + '` (' + col + ') VALUES (' + val + ');'
        self.exe(sql)
    except:
      traceback.print_exc()
    print('update item success!')



  def login(self,username,password):
    sql = 'select `uid`,`username`,`password` from `users` where `username` = "' + username + '";'
    data = self.sqlexe(sql)
    if not data:
      return 'USER_NOT_FIND' 
    if md5((username + password + '+5').encode('utf-8')) == data[0][2]:
      return data[0]
    return 'PASSWORD_ERROR'

  def register(self,username,password,email):
    sql = 'insert into `users` (`username`,`password`,`email`) VALUES ( "'+ username +'" , "'+md5((username + password + '+5').encode('utf-8'))+'","'+email+'");'
    cur = self.conn.cursor()
    data = cur.execute(sql)
    self.conn.commit()
    return data

  def changepwd(self,email,password):
    sql = 'select `uid`,`username`,`password` from `users` where `email` = "' + email + '";'
    data = self.sqlexe(sql)
    username = data[0][1]
    sql = 'update `users` set `password` = "'+ md5((username + password + '+5').encode('utf-8')) +'" where email = "'+email+'";'
    cur = self.conn.cursor()
    data = cur.execute(sql)
    self.conn.commit()
    return data

  def get_heroes(self):
    sql = 'SELECT * FROM `heroes`;'
    return self.query(sql)

  def get_items(self):
    sql = 'SELECT * FROM `items`;'
    return self.query(sql)