# -*- coding: utf-8 -*-
from . import admin
from flask import render_template, flash, request, redirect, url_for
from StudentSystem.models import User, Course
from flask_login import login_required, current_user
from .forms import SearchForm, ModifyUserForm, AddTeacherForm, \
    ChangePasswordForm, ChangeEmailForm, AddCourses
from sqlalchemy import or_, and_
from StudentSystem import db
import psutil, json


@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('admin/highchars_cpu.html')

'''
账号管理
'''
@admin.route('/teacher/user', methods=['GET', 'POST'])
@login_required
def teacher_user():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = User.query.paginate(page=page, per_page=per_page)
    teachers = pagination.items
    contxt = {
        'pagination': pagination,
        'teachers': teachers
    }
    form = SearchForm()
    if form.validate_on_submit():
        filters = {
            or_(
                User.student_id == form.info_data.data,
                User.username == form.info_data.data,
                User.email == form.info_data.data
            )

        }

        pagination = User.query.filter(*filters).paginate(page=page, per_page=per_page)
        teachers = pagination.items
        contxt = {
            'pagination': pagination,
            'teachers': teachers,
        }
        return render_template('admin/user_guanli_show.html', form=form, **contxt)
    return render_template('admin/user_guanli_show.html', form=form, **contxt)

'''
删除账户
'''
@admin.route('/teacher/<id>/delete', methods=['GET', 'POST'])
@login_required
def teacher_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('.teacher_user'))

'''
修改账号
'''
@admin.route('teacher/<id>/modify', methods=['GET', 'POST'])
@login_required
def teacher_modify(id):
    form = ModifyUserForm()
    user = User.query.filter_by(student_id=id).first()
    form.id.data = user.student_id
    form.username.data = user.username
    form.email.data = user.email
    if form.validate_on_submit():
        user.student_id=form.id.data
        user.username=form.username.data
        user.email=form.email.data
        user.password = form.password.data
        user.role=form.identify.data
        db.session.commit()
        return redirect(url_for('.teacher_user'))
    return render_template('admin/user_modify.html', form =form)

'''
添加账号
'''
@admin.route('/teacher/user/add', methods=['GET', 'POST'])
@login_required
def teacher_add():
    form = AddTeacherForm()
    form.password.data = '123465'
    if form.validate_on_submit():
        user = User(
            student_id=form.number.data,
            username=form.username.data,
            email=form.email.data,
            password = form.password.data,
            role=form.identity.data
        )
        db.session.add(user)
        db.session.commit()
        flash('添加成功')
    return render_template('admin/user_add.html', form=form)

'''
cpu实习数据
'''
@admin.route('/backstage/cpu')
@login_required
def show_cpu_data():

    return render_template('admin/highchars_cpu.html', )

@admin.route('/data')
def cpu_data():
    cpu_data = psutil.cpu_percent(1)
    data = json.dumps({'cpu': float(cpu_data)})
    return data

'''
内存实时数据
'''
@admin.route('/backstage/ram')
@login_required
def show_ram_data():
    return render_template('admin/highchars_ram.html')

@admin.route('/ram/data')
def ram_data():
    info = {}
    # 空闲内存
    free = psutil.virtual_memory().free / (1024 * 1024 * 1024)
    # 总内存
    total = psutil.virtual_memory().total / (1024 * 1024 * 1024)
    # 用过的
    used = ((psutil.virtual_memory().total - psutil.virtual_memory().free)) / (1024 * 1024 * 1024)
    # 内存使用率
    memory = float((psutil.virtual_memory().total - psutil.virtual_memory().free)) / float(
        psutil.virtual_memory().total)
    info.update({'mem_total': total, 'mem_percent': memory, 'mem_free': free, 'mem_used': used})

    return render_template('admin/_ram.html', info=info)

'''
学籍管理
'''
@admin.route('/xueji')
@login_required
def xue_ji_show():
    form = SearchForm()
    return render_template('admin/xue_ji_show.html', form=form)

'''
学籍添加
'''
@admin.route('/xueji/add')
@login_required
def xue_ji_add():
    return render_template('admin/xue_ji_add.html')


'''
个人信息管理
'''
@admin.route('/user/message')
@login_required
def user_message():
    form = SearchForm()
    return render_template('admin/ge_rens_show.html', form=form)

'''
个人信息添加
'''
@admin.route('/user/message/add')
@login_required
def add_geren_message():
    return render_template('admin/ge_rens_add.html')

'''
成绩信息
'''
@admin.route('/student/score')
@login_required
def student_score_show():
    form = SearchForm()
    return  render_template('admin/student_score_show.html', form=form)



'''
修改密码
'''
@admin.route('/change/password', methods=['GET', 'POST'])
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
    return render_template("admin/change_password.html", form=form)

'''
修改邮箱
'''
@admin.route('/change/email', methods=['GET', 'POST'])
@login_required
def change_email():
    email_form = ChangeEmailForm()
    # user = User.query.filter_by(email=email_form.old_email.data).first()
    # send_email(user.email, '修改邮箱验证码', 'auth/email/modify_email',)
    return render_template("admin/change_email.html", form=email_form)

'''
课程管理
'''
@admin.route('/course/show')
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
    form = SearchForm()
    return render_template("admin/course_show.html", form=form, **contxt)

'''
添加课程
'''
@admin.route('/course/add')
@login_required
def add_course():
    form = AddCourses()
    return render_template('admin/course_add.html', form=form)