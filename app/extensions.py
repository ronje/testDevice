# -*- coding: utf-8 -*-
# 扩展模块

"""flask_login管理用户的登录和登出,需要将我们的User模型继承flask_login的UserMixin基类"""
from flask_login import LoginManager

"""Moment 一个简单易用的轻量级JavaScript日期处理类库，提供了日期格式化、日期解析等功能"""
from flask_moment import Moment

"""flask-oauthlib第三方登录认证，如：豆瓣、QQ、reddit、google、facebook等登陆"""
from flask_oauthlib.client import OAuth

""" websocket是html5中实现了服务端和客户端进行双向文本或二进制数据通信的一种新协议"""
from flask_socketio import SocketIO

"""数据库操作"""
from flask_sqlalchemy import SQLAlchemy

"""Flask-WTF表单保护免受 CSRF 威胁"""
from flask_wtf.csrf import CSRFProtect

from flask_sockets import Sockets

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
oauth = OAuth()
sockets = Sockets()


@login_manager.user_loader
def load_user(user_id):
    from app.dataBase.models import Users
    return Users.query.get(int(user_id))


login_manager.login_view = 'auth.login'
