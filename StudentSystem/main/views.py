# -*- coding: utf-8 -*-

from . import  main
from flask import redirect, url_for, render_template, flash
from flask_login import login_user
from ..models import User
from .forms import LoginForm
from sqlalchemy import or_

@main.route('/', methods=['GET', 'POST'])
def index():
    return  render_template('index.html')

'''
登陆路由
'''
@main.route('/login', methods=['POST', 'GET'])
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
            if user.role_id == 1:
                login_user(user, form.remember.data)
                return redirect(url_for('admin.admin_index'))
            elif user.role_id == 2:
                return render_template('student/student_index.html')
            elif user.role_id == 3:
                return render_template('teacher/teacher_index.html')
        flash('你输入的学号或密码不正确')
    return render_template('main/login.html', form=form)

