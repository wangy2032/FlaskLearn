# -*- coding: utf-8 -*-

from . import db
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#用户模型
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    StudentId = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean(),default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('为了安全密码无法获得')
    #用于计算密码的hash值
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    #用于校验输入的密码和数据库你的密码是否相等
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成确认令牌
    def getToken(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    #确认令牌
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

# 用户加载函数
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#权限模型
class Role(UserMixin,db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')