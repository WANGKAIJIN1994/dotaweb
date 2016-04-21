from flask import render_template,  redirect, session, url_for, request,flash
from app import app
from dota2sql import Dota2SQL
import smtplib, base64  
from email.mime.text import MIMEText  


@app.route("/")
@app.route("/index")
def index():
    dotauser = Dota2SQL()
    steam_msg = None
    if session.get('user') is  None:
       return redirect('/login')
    else:
        steamid = dotauser.get_steamid_user(session.get('user'))
        if steamid is None:
            pass
        else:
            steam_msg = dotauser.get_steam_msg(steamid)
    return render_template("index.html",
        title = 'Home',
        steam_msg =steam_msg,
        user = session['user'])




#用户登录
@app.route('/login', methods = ['GET', 'POST'])
def login():
    dotauser = Dota2SQL()
    loginerror = ''
    if session.get('user') is not None:
       return redirect('/index')
    if request.method == 'POST':
        username = request.form["username"] 
        password = request.form["password"] 
        user =  dotauser.login(username,password)
        if user == 'USER_NOT_FIND' or user == 'PASSWORD_ERROR':
            #loginerror = 'user not find or password error';
            flash('user not find or password error')
        else:
            session['user'] = user[1]
            return redirect('/index')
    return render_template('login.html')



#用户注册
@app.route('/register', methods = ['GET', 'POST'])
def register():
    dotauser = Dota2SQL()
    go = 1
    registererror=''
    if request.method == 'POST':
        username = request.form["username"] 
        password = request.form["password"] 
        email = request.form["email"] 
        backdata = dotauser.judgeUser(username,email)
        if  backdata == 'EMAIL_EXIST':
            go = 0
            flash('This email has been registered')
        if  backdata == 'USERNAME_EXIST':
            go = 0
            flash('This username has been registered')
        if backdata == 'NOTHING_EXIST':
            sendEmail(username, password, email)    
            return redirect('/login')
    return render_template('login.html',
        error = registererror)



#用户退出登录
@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect('/index')




#注册激活的函数
@app.route("/commitRegister")
def commitRegister():
    dotauser = Dota2SQL()
    username = request.args.get('name','')
    password = request.args.get('password','')
    email = request.args.get('email','')
    dotauser.register(jiemi(username),jiemi(password),jiemi(email))
    return redirect('/login')

#更改密码
@app.route("/pwdChange", methods = ['GET', 'POST'])
def pwdChange():
    dotauser = Dota2SQL()
    if request.method == 'POST':
        password = request.form["password"] 
        email = request.form["email"] 
        username = '*'
        backdata = dotauser.judgeUser(username,email)
        if backdata == 'NOTHING_EXIST':
            flash('This email do not exist')
        else:
            sender = '18233698150@163.com'  
            message = 'password='+jiami(password)+'&email='+jiami(email)
            receiver = email
            subject = 'dodata email'  
            smtpserver = 'smtp.163.com'  
            username = '18233698150'  
            password = '1000121143'      
            msg = MIMEText('<html><h1>你好,请点击链接完成修改密码</h1><p>http://localhost:5000/pwdChangeEmail?'+message+'</p></html>','html','utf-8')      
            msg['Subject'] = subject       
            smtp = smtplib.SMTP()  
            smtp.connect('smtp.163.com')  
            smtp.login(username, password)  
            smtp.sendmail(sender, receiver, msg.as_string())  
            smtp.quit()   
            return redirect('/login')
    return render_template('findpwd.html')


#找回密码发送邮件
@app.route("/pwdChangeEmail")
def pwdChangeEmail():
    password = request.args.get('password','')
    email = request.args.get('email','')
    dotauser = Dota2SQL()
    dotauser.changepwd(jiemi(email),jiemi(password))
    return redirect('/login')


    


#发送邮件的函数，用于注册时候使用
def sendEmail(username, password, email) :   
   
    sender = '18233698150@163.com'  
    message = 'name='+jiami(username)+'&'+'password='+jiami(password)+'&'+'email='+jiami(email)
    receiver = email
    subject = 'dodata email'  
    smtpserver = 'smtp.163.com'  
    username = '18233698150'  
    password = '1000121143'      
    msg = MIMEText('<html><h1>你好,请点击链接完成登录</h1><p>http://localhost:5000/commitRegister?'+message+'</p></html>','html','utf-8')      
    msg['Subject'] = subject       
    smtp = smtplib.SMTP()  
    smtp.connect('smtp.163.com')  
    smtp.login(username, password)  
    smtp.sendmail(sender, receiver, msg.as_string())  
    smtp.quit() 

#hero
@app.route("/heroes", methods = ['GET', 'POST'])
def hero():
    dotauser = Dota2SQL()
    heroes = dotauser.get_heroes();
    abilities = dotauser.get_heroes_abilities();
    steam_msg = None
    steamid = dotauser.get_steamid_user(session.get('user'))
    if steamid is None:
        pass
    else:
        steam_msg = dotauser.get_steam_msg(steamid)
    return render_template('hero.html',
        title = 'Heroes',
        heroes = heroes,
        steam_msg =steam_msg,
        abilities = abilities,
        user = session['user'])
#goods
@app.route("/goods", methods = ['GET', 'POST'])
def goods():
    dotauser = Dota2SQL()
    items = dotauser.get_items();
    steamid = dotauser.get_steamid_user(session.get('user'))
    steam_msg = None
    steamid = dotauser.get_steamid_user(session.get('user'))
    if steamid is None:
        pass
    else:
        steam_msg = dotauser.get_steam_msg(steamid)
    return render_template('goods.html',
        title = 'Goods',
        steam_msg =steam_msg,
        items = items,
        user = session['user'])

#setting
@app.route("/setting", methods = ['GET', 'POST'])
def setting():
    dotauser = Dota2SQL()
    steamid = dotauser.get_steamid_user(session.get('user'))
    steam_msg = None
    if steamid is None:
        pass
    else:
        steam_msg = dotauser.get_steam_msg(steamid)
    user = dotauser.get_user(session['user'])
    if request.method == 'POST':
        steamid = request.form["steamid"] 
        accountid = request.form["accountid"] 
        dotauser.set_steam_id(user[0][0],int(steamid))
        dotauser.set_account_id(user[0][0],int(accountid))
    return render_template('setting.html',
        steam_msg =steam_msg,
        user = session['user'],
        title = 'Setting')


#followers
@app.route("/followers", methods = ['GET', 'POST'])
def followers():
    dotauser = Dota2SQL()
    user = dotauser.get_user(session['user'])
    followers = dotauser.get_watch_list(user[0][0])
    if request.method == 'POST':
        accountid = request.form["accountid"] 
        print(user[0][0])
        dotauser.add_watch_list(user[0][0],int(accountid))
    return render_template('followers.html',
        user = session['user'],
        followers = followers,
        title = 'Followers')


#加密算法
def jiami(str):
    b = base64.encodestring(bytes(str, 'utf-8'))
    return b.decode()


#解密算法
def jiemi(str):
     c = base64.decodestring(str.encode())
     return c.decode()
