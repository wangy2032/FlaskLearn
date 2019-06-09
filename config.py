# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    #密钥
    SECRET_KEY = 'WangYu'
    #管理员邮箱
    ADMIN_EMAIL = '884083081@qq.com'
    #主题
    FLASK_MAIL_SUBJECT_PREFIX = 'Student System'
    #发件人地址
    FLASK_MAIL_SENDER = '884083081@qq.com'
    # 邮箱服务器
    MAIL_SERVER = 'smtp.qq.com'
    # 使用TLS
    MAIL_USE_TLS = True
    # 邮箱端口
    MAIL_POST = 587
    # 邮箱账号
    MAIL_USERNAME = '884083081@qq.com'
    # qq授权码
    MAIL_PASSWORD = 'vmwfbyoitaflbehd'

    #设置上传图片的类型
    IMAGE_TYPE=['jpg', 'png', 'ico', 'jpeg']
    #设置上传文件大小
    IMAGE_SIZE = 1024*1024*64
    #设置上传路径
    IMAGE_PATH = os.path.join(basedir, 'static\\images')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost/studentsystem?auth_plugin=mysql_native_password'

config = {
    'DevelopmentConfig':DevelopmentConfig
}
