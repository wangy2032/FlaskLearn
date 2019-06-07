# -*- coding: utf-8 -*-

from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from ..models import User
from . import auth
from StudentSystem import db
from .forms import LoginForm, AddUserForm, ChangePasswordForm, \
    ChangeEmailForm, AddStudentForm, SearchForm, RetrievePasswordForm, GetCode
from StudentSystem.sendEmail import send_email, MyRedis
import string
import random
from datetime import datetime

my_redis = MyRedis.connect()

'''
主页路由
'''
@auth.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

'''
登陆路由
'''
@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        filters = {
            or_(
                User.student_id == form.id.data
            )
        }
        user = User.query.filter(*filters).first()
        if user is not None and user.verify_password(form.password.data.strip()):
            if user.role == 'admin':
                login_user(user, form.remember.data)
                user.new_login_time = datetime.now()
                user.login_number += 1
                db.session.commit()
                return redirect(url_for('admin.index'))
            elif user.role == 'student':
                login_user(user, form.remember.data)
                user.new_login_time = datetime.now()
                user.login_number += 1
                db.session.commit()
                return redirect(url_for('student.index'))
            elif user.role == 'teacher':
                login_user(user, form.remember.data)
                user.new_login_time = datetime.now()
                user.login_number += 1
                db.session.commit()
                return redirect(url_for('teacher.index'))
        flash('你输入的学号或密码不正确')
    return render_template('auth/login.html', form=form)

'''
退出登陆
'''
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))



'''
邮件确认
'''
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.base'))
    if current_user.confirm(token):
        db.session.commit()
        flash('账户确认成功')
    else:
        flash('确认链接无效或者已过期')
    return redirect(url_for('main.base'))

'''
修改密码
'''
@auth.route('/ChangePassword', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码重设成功')
            return redirect(url_for('main.base'))
        else:
            flash('原密码不正确')
    return render_template("auth/change_password.html", form=form)

'''
修改邮箱
'''
@auth.route('/change/email', methods=['GET', 'POST'])
@login_required
def change_email():
    email_form = ChangeEmailForm()
    # user = User.query.filter_by(email=email_form.old_email.data).first()
    # send_email(user.email, '修改邮箱验证码', 'auth/email/modify_email',)
    return render_template("auth/change_email.html", form=email_form)




'''
找回密码路由
'''
@auth.route('/retrieve-password/send-code')
def send_code_email():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    zi_mu_list = list(string.ascii_letters)
    zi_mu_list.extend(map(lambda x: str(x), range(0, 10)))
    code = "".join(random.sample(zi_mu_list, 6))
    MyRedis.set_cache_data(my_redis, email, code)
    send_email(email, '邮箱验证码', 'auth/email/modify_email', user=user, code=code)

@auth.route('/retrieve-password', methods=['POST', 'GET'])
def retrieve_password():
    form = RetrievePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(student_id=form.id.data).first()
        email = form.email.data
        if user and user.email == email:
            if form.yan_zheng_ma.data == MyRedis.get_cache_data(my_redis, email):
                user.password = form.password.data
                db.session.add(user)
                db.session.commit()
                flash('修改成功')
                return redirect(url_for('auth.login'))
            else:
                flash('验证码不正确！')
                return render_template('auth/forget_password.html', form=form)
        flash('用户不存在或邮箱不正确！')
    return render_template('auth/forget_password.html', form=form)



