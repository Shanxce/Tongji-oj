from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_mail import Mail, Message

import os
basedir = os.path.dirname(os.path.abspath(__file__))

# flask_login
app = Flask(__name__)
login_manager = LoginManager(app)  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'user.UserLogin'  # 设置用户登录视图函数 endpoint
login_manager.session_protection = 'basic'
login_manager.login_message = u"请先登录。"
app.secret_key = "ASDF"

# flask_mail
app.config['MAIL_SERVER'] = 'smtp.163.com'       #电子邮件服务器的名称
app.config['MAIL_USERNAME'] = 'tongjioj@163.com'        #发件人用户名
app.config['MAIL_PASSWORD'] = 'LGAWOFKEWOSRCGHW'    #发件人密码
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)