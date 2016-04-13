from flask import render_template,  redirect, session, url_for, request
from app import app, dota


@app.route("/")
@app.route("/index")
def index():
    if session.get('user') is  None:
       return redirect('/login')
    return render_template("index.html",
        title = 'Home',
        user = session['user'])




#用户登录
@app.route('/login', methods = ['GET', 'POST'])
def login():
    dotauser = dota.dota2sql()
    loginerror = ''
    if session.get('user') is not None:
       return redirect('/index')
    if request.method == 'POST':
        username = request.form["username"] 
        password = request.form["password"] 
        user =  dotauser.login(username,password)
        if user == 'USER_NOT_FIND' or user == 'PASSWORD_ERROR':
            loginerror = 'user not find or password error';
        else:
            session['user'] = user[1]
            return redirect('/index')
    return render_template('login.html',
        error = loginerror)



#用户注册
@app.route('/register', methods = ['GET', 'POST'])
def register():
    dotauser = dota.dota2sql()
    if request.method == 'POST':
        username = request.form["username"] 
        password = request.form["password"] 
        dotauser.register(username,password)
        return redirect('/login')
    return render_template('login.html',
        title = 'Sign In')



#用户退出登录
@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect('/index')


@app.route("/competition")
def competition():
    return render_template("competition.html")

@app.route("/goods")
def goods():
    return render_template("goods.html")

@app.route("/hero")
def hero():
    return render_template("hero.html")

@app.route("/sendmail")
def sendmail():
    return '<h1>sending...</h1>'