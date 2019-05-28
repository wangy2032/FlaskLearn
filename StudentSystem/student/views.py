# -*- coding: utf-8 -*-
from . import student
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from StudentSystem import db
from StudentSystem.auth.forms import ChangeEmailForm, ChangePasswordForm


'''
基本信息
'''
@student.route('/ji-ben-msg')
@login_required
def index():

    return render_template('student/ji_ben_msg.html')

'''
学籍信息
'''
@student.route('/xue-ji-msg')
@login_required
def xue_ji_show():
    return render_template('student/xue_ji_msg.html')


'''
修改密码
'''
@student.route('/ChangePassword', methods=['GET', 'POST'])
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
    return render_template("student/change_password.html", form=form)

'''
修改邮箱
'''
@student.route('/change/email', methods=['GET', 'POST'])
@login_required
def change_email():
    email_form = ChangeEmailForm()
    # user = User.query.filter_by(email=email_form.old_email.data).first()
    # send_email(user.email, '修改邮箱验证码', 'auth/email/modify_email',)
    return render_template("student/change_email.html", form=email_form)

'''
我的课程
'''

