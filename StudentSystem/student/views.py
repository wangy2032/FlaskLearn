# -*- coding: utf-8 -*-
from . import student
from flask import render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from StudentSystem.models import db, Geren, Xueji, Course, Score, User
from StudentSystem.student.forms import ChangeEmailForm, ChangePasswordForm, SearchForm
from sqlalchemy import or_
from StudentSystem.sendEmail import send_email, MyRedis
import string, random

'''
基本信息
'''
@student.route('/ji-ben-msg')
@login_required
def index():
    print(current_user.student_id)
    student_ji_ben = Geren.query.filter_by(student_id=current_user.student_id).first()
    print(student)
    return render_template('student/ji_ben_msg.html', student_ji_ben=student_ji_ben)

'''
学籍信息
'''
@student.route('/xue-ji-msg')
@login_required
def xue_ji_show():
    student_xue_ji = Xueji.query.filter_by(student_id=current_user.student_id).first()
    return render_template('student/xue_ji_msg.html', student_xue_ji=student_xue_ji)

"""
选课
"""
@student.route('/course/show', methods=['GET', 'POST'])
@login_required
def course_show():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Course.query.paginate(page=page, per_page=per_page)
    courses = pagination.items
    contxt = {
        'pagination': pagination,
        'courses': courses
    }
    ge_ren_courses = Score.query.filter_by(student_id=current_user.student_id).all()
    form = SearchForm()
    if form.validate_on_submit() and form.info_data.data:
        filters = {or_(Course.course_id == form.info_data.data.strip(),
                       Course.course_name == form.info_data.data.strip())}
        pagination = Course.query.filter(*filters).paginate(page=page, per_page=per_page)
        courses = pagination.items
        contxt = {
            'pagination': pagination,
            'courses': courses,
        }
        return render_template('student/course_add.html', form=form, **contxt, ge_ren_courses=ge_ren_courses)
    return render_template('student/course_add.html', form=form, **contxt, ge_ren_courses=ge_ren_courses)

@student.route('/course/<course_id>/add')
@login_required
def course_add(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    couse_check = Score.query.filter_by(course_id=course_id).first()
    if not couse_check:
        add_score = Score(
            student_id=current_user.student_id,
            course_id=course.course_id,
            course_name=course.course_name,
            course_credit=course.course_credit,
            teacher_id=course.teacher_id,
            teacher=course.teacher,
            class_room=course.class_room,
            course_time=course.course_time
        )
        db.session.add(add_score)
        db.session.commit()
        flash('{}课程添加成功'.format(course.course_name))
    flash('此课程以添加！')
    return redirect(url_for('student.course_show'))



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
            return redirect(url_for('student.change_password'))
        else:
            flash('原密码不正确')
    return render_template("student/change_password.html", form=form)

'''
修改邮箱
'''
my_redis = MyRedis.connect()
@student.route('/retrieve-password/send-code')
def send_code_email():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        zi_mu_list = list(string.ascii_letters)
        zi_mu_list.extend(map(lambda x: str(x), range(0, 10)))
        code = "".join(random.sample(zi_mu_list, 6))
        MyRedis.set_cache_data(my_redis, email, code)
        send_email(email, '邮箱验证码', 'auth/email/modify_email', user=user, code=code)
        return jsonify({'data':1})
    return jsonify({'data': 0})

@student.route('/change/email', methods=['GET', 'POST'])
@login_required
def change_email():
    email_form = ChangeEmailForm()
    user = User.query.filter_by(email=email_form.old_email.data).first()
    if user:
        send_email(user.email, '修改邮箱验证码', 'auth/email/modify_email',)
    if email_form.validate_on_submit():
        user.email = email_form.new_email.data
        db.session.commit()
    return render_template("student/change_email.html", form=email_form)

'''
我的课程
'''

