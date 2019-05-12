# -*- coding: utf-8 -*-
from . import admin
from flask import render_template, flash, request, redirect, url_for
from ..models import User
from flask_login import login_required
from .forms import SearchForm, ModifyUserForm, AddTeacherForm
from sqlalchemy import or_, and_
from ..models import db
import psutil, json

'''
老师账号管理
'''
@admin.route('/', methods=['GET', 'POST'])
@login_required
def admin_index():

    return render_template('admin/admin_index.html')

'''
老师账号管理
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
                User.StudentId == form.info_data.data,
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
        return render_template('admin/teacher_user.html', form=form, **contxt)
    return render_template('admin/teacher_user.html', form=form, **contxt)

'''
删除路由
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
    user = User.query.filter_by(StudentId=id).first()
    form.id.data = user.StudentId
    form.username.data = user.username
    form.email.data = user.email
    if form.validate_on_submit():
        user.StudentId=form.id.data
        user.username=form.username.data
        user.email=form.email.data
        user.password = form.password.data
        user.role_id=form.identify.data
        db.session.commit()
        return redirect(url_for('.teacher_user'))
    return render_template('admin/modify_teacher.html', form =form)

'''
添加老师账号
'''
@admin.route('/teacher/user/add', methods=['GET', 'POST'])
@login_required
def teacher_add():
    form = AddTeacherForm()
    form.password.data = '123465'
    if form.validate_on_submit():
        user = User(
            StudentId=form.number.data,
            username=form.username.data,
            email=form.email.data,
            password = form.password.data,
            role_id=form.identity.data
        )
        db.session.add(user)
        db.session.commit()
        flash('添加成功')
    return render_template('admin/add_teacher.html', form=form)

'''
cpu实习数据
'''
@admin.route('/backstage/cpu')
@login_required
def show_cpu_data():

    return render_template('admin/cpu_highchars.html', )

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

    return render_template('admin/ram_highchars.html')

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