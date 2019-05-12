# -*- coding: utf-8 -*-
from . import admin
from flask import render_template, flash, request, redirect, url_for
from ..models import User
from flask_login import login_required
from .forms import SearchForm, ModifyUserForm
from sqlalchemy import or_, and_
from ..models import db

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
    per_page = 2
    pagination = User.query.filter_by(role_id=2).paginate(page=page, per_page=per_page)
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

        pagination = User.query.filter_by(role_id=2).filter(*filters).paginate(page=page, per_page=per_page)
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
    return render_template('admin/modify_teacher.html', form =form)