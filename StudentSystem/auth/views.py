# -*- coding: utf-8 -*-

from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from ..models import User
from . import auth
from StudentSystem import db
from .forms import LoginForm, RegisteredForm, ChangePasswordForm
from ..sendEmail import send_email

'''
登陆路由
'''
@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        filters = {
            or_(
                User.StudentId == form.StudentId.data,
                User.email == form.StudentId.data,
            )
        }
        user = User.query.filter(*filters).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(url_for('main.base'))
        else:
            flash('你输入的学号或密码不正确')
    return render_template('auth/login.html', form=form)

'''
退出登陆
'''
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

'''
注册路由
'''
@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisteredForm()
    if form.validate_on_submit():
        print('你好')
        user = User(StudentId=form.StudentId.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.getToken()
        send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user, token=token)
        flash('注册成功,确认邮件已发送至你的邮箱')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)

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










