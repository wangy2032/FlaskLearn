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
            return redirect(url_for('auth.shou_ye'))
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
添加账户
'''
@auth.route('/add_user', methods=['GET','POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(StudentId=form.student_id.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.getToken()
        send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user, token=token)
        flash('注册成功,确认邮件已发送至你的邮箱')
        # return redirect(url_for('.login'))
    return render_template('auth/add_user.html', form=form)


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
账号显示
'''
@auth.route('/remove_user', methods=['GET', 'POST'])
@login_required
def remove_user():
    users = User.query.all()
    return render_template('auth/remove_user.html', users=users)


'''
新增学生
'''
@auth.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudentForm()
    return render_template('auth/add_student.html', form=form)

'''
首页
'''
@auth.route('/shou_ye', methods=['GET', 'POST'])
@login_required
def shou_ye():
    return render_template('auth/shou_ye.html')


'''
学生信息
'''
@auth.route('/student_message', methods=['GET', 'POST'])
@login_required
def student_message():
    form = SearchForm()
    if form.validate_on_submit():
        if form.student_number.data:
            json_data = {
                'id': 1,
                'number': 15111202032,
                'name': '对话',
                'email': '884083081@qq.com',
                'iphone': 15266489360,
                'address': '贵州省遵义市'
            }
            return render_template('auth/student_message.html', json_data=json_data, form=form)
        return render_template('auth/student_message.html', form=form)
    return render_template('auth/student_message.html', form=form)

'''
找回密码路由
'''
@auth.route('/retrieve_password')
def retrieve_password():
    form = RetrievePasswordForm()
    return render_template('auth/forget_password.html', form=form)



