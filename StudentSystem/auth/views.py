# -*- coding: utf-8 -*-

from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from ..models import User
from . import auth
from StudentSystem import db
from .forms import LoginForm, AddUserForm, ChangePasswordForm, \
    ChangeEmailForm, AddStudentForm, SearchForm, RetrievePasswordForm
from ..sendEmail import send_email


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
            print('a')
            if user.role == '管理员':
                login_user(user, form.remember.data)
                return redirect(url_for('admin.index'))
            elif user.role == '学生':
                login_user(user, form.remember.data)
                return redirect(url_for('student.index'))
            elif user.role_id == 3:
                return render_template('teacher/teacher_index.html')
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
@auth.route('/retrieve_password')
def retrieve_password():
    form = RetrievePasswordForm()
    return render_template('auth/forget_password.html', form=form)



