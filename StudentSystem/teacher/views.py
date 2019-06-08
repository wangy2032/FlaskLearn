# -*- coding: utf-8 -*-
from . import teacher
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from StudentSystem import db
from StudentSystem.models import Geren, Xueji, Student
from StudentSystem.teacher.forms import StudentJiBenMsg, StudentXueJi, \
    SearchForm, StudentJiBenMdifyMsg, StudentXueJiModify


"""
录入学生信息
"""
@teacher.route('/ji-ben-msg/add', methods=['GET', 'POST'])
@login_required
def index():
    form = StudentJiBenMsg()
    search_form = SearchForm()
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
    return render_template('teacher/add_student_jiben.html',search_form=search_form, form=form, **contxt)

@teacher.route('/<student_id>/ji-ben-msg/show', methods=['GET','POST'])
@login_required
def show(student_id):
    '''
    查看基本信息
    '''
    geren = Geren.query.filter_by(student_id=student_id).first()
    form = StudentJiBenMdifyMsg()
    if form.validate_on_submit():
        if form.modify.data:
            geren.student_id = form.student_id.data
            geren.name = form.name.data
            geren.user_name = form.used_name.data
            geren.sex = form.sex.data
            geren.id_type = form.id_type.data
            geren.id_number = form.id_number.data
            form.birth_time.data = geren.date_of_birth
            geren.min_zu = form.nation.data
            geren.p_status = form.p_status.data
            geren.a_time = form.ad_time.data
            geren.birthplace = form.b_place.data
            geren.a_location = form.acc_location.data
            geren.student_id = form.stu_source.data
            geren.place_of_birth = form.bir_address.data
            db.session.commit()
            flash('更新成功')
            return redirect(url_for('teacher.index'))
    form.student_id.data = geren.student_id
    form.name.data =geren.name
    form.used_name.data = geren.user_name
    form.sex.data = geren.sex
    form.id_type.data = geren.id_type
    form.id_number.data = geren.id_number
    form.birth_time.data = geren.date_of_birth
    form.nation.data = geren.min_zu
    form.p_status.data = geren.p_status
    form.ad_time.data = geren.a_time
    form.b_place.data = geren.birthplace
    form.acc_location.data = geren.a_location
    form.stu_source.data = geren.student_id
    form.bir_address.data = geren.place_of_birth
    return render_template('teacher/show_geren_msg.html', form=form, geren=geren)

'''
录入学生学籍
'''
@teacher.route('/xue-ji/add', methods=['GET', 'POST'])
@login_required
def add_xueji():
    form = StudentXueJi()
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Xueji.query.paginate(page=page, per_page=per_page)
    xuejis = pagination.items
    contxt = {
        'pagination': pagination,
        'xuejis': xuejis
    }
    if form.validate_on_submit():
        student = Student.query.filter_by(student_id=form.student_id.data).first()
        if student:
            xueji_user = Xueji(
                name = form.name.data,
                student_id= form.student_id.data,
                school_year = form.school_year.data,
                semester = form.semester.data,
                grade = form.grade.data,
                college_name = form.college_name.data,
                d_name = form.d_name.data,
                p_name = form.p_name.data,
                class_name = form.class_name.data,
                school_system = form.school_system.data,
                xue_ji_zt = form.xue_ji_zt.data,
                zai_xiao = form.zai_xiao.data,
                e_level = form.e_level.data,
                t_method = form.t_method.data,
                student_type = form.student_type.data,
                a_college = form.a_college.data,
                a_profession = form.a_profession.data
            )
            db.session.add(xueji_user)
            db.session.commit()
        else:
            flash('学生不存在！')
        return redirect(url_for('teacher.add_xueji'))
    return  render_template('teacher/add_student_xueji.html',search_form=search_form, form=form, **contxt)

@teacher.route('/<student_id>/xue-ji/show', methods=['GET','POST'])
@login_required
def show_xueji(student_id):
    '''
    显示学籍信息
    '''
    student = Xueji.query.filter_by(student_id=student_id).first()
    form = StudentXueJiModify()
    if form.validate_on_submit():
        student.name = form.name.data
        student.student_id = form.student_id.data
        student.school_year = form.school_year.data
        student.semester = form.semester.data
        student.grade = form.grade.data
        student.college_name = form.college_name.data
        student.d_name = form.d_name.data
        student.p_name = form.p_name.data
        student.class_name = form.class_name.data
        student.school_system = form.school_system.data
        student.xue_ji_zt = form.xue_ji_zt.data
        student.zai_xiao = form.zai_xiao.data
        student.e_level = form.e_level.data
        student.t_method = form.t_method.data
        student.student_type = form.student_type.data
        student.a_college = form.a_college.data
        student.a_profession = form.a_profession.data
        db.session.commit()
        flash('更新成功')
        return redirect(url_for('teacher.add_xueji'))
    form.name.data = student.name
    form.student_id.data = student.student_id
    form.school_year.data = student.school_year
    form.semester.data = student.semester
    form.grade.data = student.grade
    form.college_name.data = student.college_name
    form.d_name.data = student.d_name
    form.p_name.data = student.p_name
    form.class_name.data = student.class_name
    form.school_system.data = student.school_system
    form.xue_ji_zt.data = student.xue_ji_zt
    form.zai_xiao.data = student.zai_xiao
    form.e_level.data = student.e_level
    form.t_method.data = student.t_method
    form.student_type.data = student.student_type
    form.a_college.data = student.a_college
    form.a_profession.data = student.a_profession
    return render_template('teacher/show_xueji_msg.html', student=student, form=form)

'''
录入学生成绩
'''
@teacher.route('/score/add')
@login_required
def add_score():
    return  render_template('teacher/add_student_score.html')