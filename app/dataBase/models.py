# -*- coding: utf-8 -*-
#数据库 表 模块

import hashlib
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager


class Users(UserMixin, db.Model):
    __tablename__ = "t_users"
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(128))
    email = db.Column(db.String(254), unique=True, nullable=False)
    nickname = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    email_hash = db.Column(db.String(128))
    phone = db.Column(db.Integer)
    addr = db.Column(db.String(255))
    login_time = db.Column(db.DateTime)
    devices = db.relationship('Devices', back_populates='users', cascade='all')

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        self.generate_email_hash()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_email_hash(self):
        if self.email is not None and self.email_hash is None:
            self.email_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()  # encode for py23 compatible

    def up_logintime(self,logntime):
        self.login_time = logntime

    @property  #@property装饰器来创建只读属性
    def is_admin(self):
        return self.email == current_app.config['CATCHAT_ADMIN_EMAIL']

class Roles(db.Model):
    __tablename__ = "t_roles"
    id = db.Column(db.Integer, primary_key=True)
    name = mac = db.Column(db.String(12), nullable=False)

#未登陆时的用户模型
class Guest(AnonymousUserMixin):

    @property
    def is_admin(self):
        return False

login_manager.anonymous_user = Guest

class Devices(db.Model):
    __tablename__ = "t_devices"
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(12), unique=True, nullable=False)
    model = db.Column(db.String(60))
    update_interval = db.Column(db.Integer,default=1200)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.relationship('Messages', back_populates='devices')

class Messages(db.Model):
    __tablename__ = "t_messages"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(60), default=datetime.utcnow)
    connect_time = db.Column(db.DateTime)
    disonnect_time = db.Column(db.DateTime)
    last_update_time = db.Column(db.DateTime)
    current_update_time = db.Column(db.DateTime, index=True)
    update_interval = db.Column(db.Integer,default=1200)
    timeout = db.Column(db.Integer,default=0)
    timeout_count = db.Column(db.Integer)
    connet_count = db.Column(db.Integer)
    data = db.Column(db.String(256))
    mac_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    # device = db.relationship('Devices', back_populates='messages')
