from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import LoginManager, login_user, UserMixin, current_user, login_required, logout_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import datetime
import sqlite3 as sql
import os
import random
import re
from website.login import user_bp
from website import login_manager, app, mail
from website.login.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@user_bp.route("/user/register/")
def Register():
    return render_template('register.html')   #前端直接写url_for('ResterResult')即可


@user_bp.route("/user/registerresult/", methods = ['POST'])
def RegisterResult():
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
 
    user_name = request.form['name']   #获取表单昵称
    user_email = request.form['email']   #获取表单邮箱，并查阅数据库确认不重复
    print(user_name)
    print(user_email)
    cur.execute('select * from UserInfo where user_email = ?', (user_email,))
    con.commit()
    fetched_email = cur.fetchone()
    if fetched_email != None:
        #flash('This email has been registered, please change one!')
        flash('该邮箱已经被注册，请更换一个邮箱！')
        return redirect(url_for('user.Register'))
    
    passwd = request.form['passwd']
    repasswd = request.form['repasswd']
    token = request.form['verify_code']
    if user_name == '' or user_email == '' or passwd == '' or repasswd == '' or token == '':
        flash('请填写以上所有信息！')
        return redirect(url_for('user.Register'))

    if passwd != repasswd:
        #flash('The two passwords are not the same! Please input again')
        flash('前后密码输入不一致！请确认后重新输入')
        return redirect(url_for('user.Register'))
    
    if token != mails_list[user_email][0]:
        flash('验证码错误！')
        return redirect(url_for('user.Register'))

    user_password = generate_password_hash(passwd)   #获取表单密码 
    user_identity = 3
    user_head = "/static/img/head/"+str(random.randint(1,6))+".jpg"

    cur.execute('insert into UserInfo values(NULL, ?, ?, ?, ?, ?, ?)', (user_name, user_email, user_password, user_identity, user_head, \
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    con.commit()
    con.close()   #写入后关闭
    flash('注册成功！')
    return redirect(url_for('user.UserLogin'))


mails_list = {}
@user_bp.route("/user/register/email/", methods = ['POST'])
def SendEmail():
    user_email = request.form['email']

    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", user_email):
        return {'code': 400, 'msg': '邮箱地址非法'}
    
    msg = Message('TJ-oj注册邮箱验证码', sender = 'tongjioj@163.com', recipients = [user_email])
    code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for _ in range(6))
    msg.body = f'''您的验证码为：{code}
-----------------------------
验证码在10分钟内有效
-----------------------------
'''
    with app.app_context():
        mail.send(msg)
    mails_list[user_email] = (code, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #return redirect(url_for('user.Register'))   #这里register界面填写过的内容可能会清空吧？
    return {'code': '200'}


@user_bp.route("/user/login/")
def UserLogin():
    return render_template("login.html") 


@user_bp.route("/user/loginresult/", methods = ['POST'])
def LoginResult():
    email = request.form['email']
    password = request.form['password']
    if password == '' or email == '':
        #flash('please input your email and password!')
        flash('请输入您的邮箱和密码！')
        return redirect(url_for('user.UserLogin'))
    
    con = sql.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "online_judge.db")) 
    cur = con.cursor()
    cur.execute("select * from UserInfo where user_email = ?", (email,))
    con.commit()
    user_info = cur.fetchone()
    if user_info == None:
        #flash('User is not registered!')
        flash('该用户未被注册！请先注册')
        return redirect(url_for('user.UserLogin'))

    col_name_user = [tuple[0] for tuple in cur.description]
    user = dict(zip(col_name_user, user_info))           #user的dictionary，可用来初始化User类
    loginUser = User(user)
    if loginUser.VerrifyPassword(password) == False:
        #flash('Password is not correct!')
        flash('账号或密码不正确！请重新输入')
        return redirect(url_for('user.UserLogin'))
    
    login_user(loginUser)
    con.close()
    return redirect(url_for('home.home'))      #跳转到题目界面


@user_bp.route("/user/logout/")
@login_required
def UserLogout():
    logout_user()
    flash("退出成功，请重新登录！")
    return redirect(url_for('user.UserLogin'))

