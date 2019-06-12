# -*- coding: utf-8 -*-
#应用包的构造函数

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config, Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES



bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['MAX_CONTENT_LENGTH'] = Config.IMAGE_SIZE
    app.config['UPLOADED_PHOTOS_DEST'] = Config.IMAGE_PATH
    # app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL
    app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
    app.config['MAIL_PORT'] = Config.MAIL_POST
    app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
    global file
    file = UploadSet('photos', IMAGES)
    configure_uploads(app, file)
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)


    #注册登陆蓝本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    #注册管理员蓝本
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    #注册学生蓝图
    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/student')
    #注册老师蓝图
    from .teacher import teacher as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/teacher')

    return app

