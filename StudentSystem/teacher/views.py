# -*- coding: utf-8 -*-
from . import teacher
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from StudentSystem import db
from StudentSystem.models import Geren
from StudentSystem.teacher.forms import StudentJiBenMsg
from datetime import datetime


'''
录入学生信息
'''
@teacher.route('/ji-ben-msg/add', methods=['GET', 'POST'])
@login_required
def index():
    form = StudentJiBenMsg()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Geren.query.paginate(page=page, per_page=per_page)
    gerens = pagination.items
    contxt = {
        'pagination': pagination,
        'gerens': gerens
    }
    if form.validate_on_submit():
        if form.ti_jiao.data:
            geren = Geren(
                student_id=form.student_id.data,
                name=form.name.data,
                user_name=form.used_name.data,
                sex=form.sex.data,
                id_type=form.id_type.data,
                id_number=form.id_number.data,
                date_of_birth=form.birth_time.data,
                min_zu=form.nation.data,
                p_status=form.p_status.data,
                a_time=form.ad_time.data,
                birthplace=form.b_place.data,
                a_location=form.acc_location.data,
                s_source=form.stu_source.data,
                place_of_birth=form.bir_address.data
            )
            db.session.add(geren)
            db.session.commit()
            flash('添加成功！')
        elif form.chong_zhi.data:
            flash('重置成功！')
            return redirect(url_for('teacher.index'))
    return render_template('teacher/add_student_jiben.html', form=form, **contxt)

'''
查看基本信息
'''
@teacher.route('/<student_id>/ji-ben-msg/show')
@login_required
def show(student_id):
    geren = Geren.query.filter_by(student_id=student_id).first()
    form = StudentJiBenMsg()
    form.student_id.data = geren.student_id
    form.name.data =geren.name
    form.used_name.data = geren.user_name
    form.sex.data = geren.sex
    form.id_type.data = geren.id_type
    form.id_number.data = geren.id_number
    form.birth_time.data = datetime.strptime(geren.date_of_birth, '%Y-%m-%d')
    form.nation.data = geren.min_zu
    form.p_status.data = geren.p_status
    form.ad_time.data = datetime.strptime(geren.a_time, '%Y-%m-%d')
    form.b_place.data = geren.birthplace
    form.acc_location.data = geren.a_location
    form.stu_source.data = geren.student_id
    form.bir_address.data = geren.place_of_birth
    return render_template('teacher/show_geren_msg.html', form=form, geren=geren)