# -*- coding: utf-8 -*-
import csv

from flask_admin._compat import csv_encode

from . import admin
from flask import render_template, flash, request, redirect, url_for, jsonify, Response, make_response, stream_with_context
from StudentSystem.models import User, Course, Geren, Student, Teacher, Xueji, db, Score
from flask_login import login_required, current_user
from .forms import SearchForm, ModifyUserForm, AddTeacherForm, \
    ChangePasswordForm, ChangeEmailForm, AddCourses, StudentJiBenMsg, \
    StudentXueJi, ModifyCourses, ScoreForm, StudentXueJiModify, StudentJiBenMsgModify
from sqlalchemy import or_, and_
import psutil, json, string, redis, random
from StudentSystem.sendEmail import send_email,MyRedis
import codecs



@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('admin/highchars_cpu.html')

"""
后台监控
"""
@admin.route('/backstage/cpu')
@login_required
def show_cpu_data():
    '''
    cpu实时数据展示
    :return:
    '''
    return render_template('admin/highchars_cpu.html', )

@admin.route('/data')
def cpu_data():
    '''
    cpu数据回调js
    :return:
    '''
    cpu_data = psutil.cpu_percent(1)
    data = json.dumps({'cpu': float(cpu_data)})
    return data

@admin.route('/backstage/ram')
@login_required
def show_ram_data():
    '''
    内存实时数据展示
    '''
    return render_template('admin/highchars_ram.html')

@admin.route('/ram/data')
def ram_data():
    '''
    获取内存数据
    :return:
    '''
    info = {}
    free = psutil.virtual_memory().free / (1024 * 1024 * 1024)# 空闲内存
    total = psutil.virtual_memory().total / (1024 * 1024 * 1024)# 总内存
    used = ((psutil.virtual_memory().total - psutil.virtual_memory().free)) / (1024 * 1024 * 1024) # 用过的
    memory = float((psutil.virtual_memory().total - psutil.virtual_memory().free)) / float(
        psutil.virtual_memory().total)# 内存使用率
    info.update({'mem_total': total, 'mem_percent': memory, 'mem_free': free, 'mem_used': used})
    return render_template('admin/_ram.html', info=info)

"""
账号信息
"""
@admin.route('/teacher/user', methods=['GET', 'POST'])
@login_required
def account_number_show():
    '''
    显示账号管理页面
    :return:
    '''
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = User.query.paginate(page=page, per_page=per_page)
    teachers = pagination.items
    contxt = {
        'pagination': pagination,
        'teachers': teachers
    }
    form = SearchForm()
    if form.validate_on_submit() and form.info_data.data:
        filters = {or_(User.student_id == form.info_data.data.strip(),
                User.username == form.info_data.data.strip(),
                User.email == form.info_data.data.strip(),
                User.role == form.info_data.data.strip())}
        pagination = User.query.filter(*filters).paginate(page=page, per_page=per_page)
        teachers = pagination.items
        contxt = {
            'pagination': pagination,
            'teachers': teachers,
        }
        return render_template('admin/user_show.html', form=form, **contxt)
    return render_template('admin/user_show.html', form=form, **contxt)

@admin.route('/student/<id>/delete', methods=['GET', 'POST'])
@login_required
def teacher_delete(id):
    '''
    删除账户按钮路由
    '''
    user = User.query.filter_by(student_id=id).first()
    if user.role == 'teacher':
        teacher = Teacher.query.filter_by(teacher_id=id).first()
        courses = Course.query.filter_by(teacher_id=id).all()
        if courses:
            for course in courses:
                db.session.delete(course)
        if teacher:
            db.session.delete(teacher)
    if user.role == 'student':
        student = Student.query.filter_by(student_id=id).first()
        geren = Geren.query.filter_by(student_id=id).first()
        xj = Xueji.query.filter_by(student_id=id).first()
        scores = Score.query.filter_by(student_id=id).all()
        if scores:
            for score in scores:
                db.session.delete(score)
        if geren:
            db.session.delete(geren)
        if xj:
            db.session.delete(xj)
        if student:
            db.session.delete(student)
    db.session.delete(user)
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('admin.account_number_show'))

@admin.route('student/<id>/modify', methods=['GET', 'POST'])
@login_required
def teacher_modify(id):
    '''
    修改账号按钮路由
    '''
    form = ModifyUserForm()
    user = User.query.filter_by(student_id=id).first()
    if form.validate_on_submit():
        user.student_id=form.id.data
        user.username=form.username.data
        user.email=form.email.data
        if form.password.data:
            user.password = form.password.data
        user.role=form.identify.data
        print(form.identify.data)
        if form.identify.data == 'teacher':
            teacher_tmp = Teacher.query.filter_by(teacher_id=form.id.data).first()
            if not teacher_tmp:
                teacher = Teacher(teacher_id=form.id.data, name=form.username.data)
                tmp = Student.query.filter_by(student_id=form.id.data).first()
                if tmp:
                    db.session.delete(tmp)
                db.session.add(teacher)
        if form.identify.data == 'student':
            student_tmp = Student.query.filter_by(student_id=form.id.data).first()
            if not student_tmp:
                student = Student(student_id=form.id.data, name=form.username.data)
                tmp = Teacher.query.filter_by(teacher_id=form.id.data).first()
                course_tmp = Course.query.filter_by(teacher_id=form.id.data).all()
                if tmp:
                    for i in course_tmp:
                        db.session.delete(i)
                    db.session.delete(tmp)
                db.session.add(student)
        db.session.commit()
        flash('更新成功')
        return redirect(url_for('.account_number_show'))
    form.id.data = user.student_id
    form.username.data = user.username
    form.email.data = user.email
    form.identify.data = user.role
    return render_template('admin/user_modify.html', form =form)

@admin.route('/teacher/user/add', methods=['GET', 'POST'])
@login_required
def teacher_add():
    '''
    添加账号按钮路由
    '''
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
        if form.identity.data == 'student':
            student_tmp = Student.query.filter_by(student_id=form.number.data).first()
            if not student_tmp:
                student = Student(student_id=form.number.data, name=form.username.data)
                db.session.add(student)
        elif form.identity.data == 'teacher':
            teacher_tmp = Teacher.query.filter_by(teacher_id=form.number.data).first()
            if not teacher_tmp:
                teacher = Teacher(teacher_id=form.number.data, name=form.username.data)
                db.session.add(teacher)
        db.session.add(user)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('admin.account_number_show'))
    return render_template('admin/user_add.html', form=form)



"""
基本信息
"""
@admin.route('/user/message', methods=['GET','POST'])
@login_required
def user_message():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Geren.query.paginate(page=page, per_page=per_page)
    students = pagination.items
    contxt = {
        'pagination': pagination,
        'students': students
    }
    form = SearchForm()
    if form.validate_on_submit() and form.info_data.data:
        filters = {or_(Geren.student_id == form.info_data.data.strip(),
                       Geren.name == form.info_data.data.strip())}
        pagination = Geren.query.filter(*filters).paginate(page=page, per_page=per_page)
        students = pagination.items
        contxt = {
            'pagination': pagination,
            'students': students,
        }
        return render_template('admin/ge_rens_show.html', form=form, **contxt)
    return render_template('admin/ge_rens_show.html', form=form, **contxt)

@admin.route('/user/message/add', methods=['GET','POST'])
@login_required
def add_geren_message():
    '''
    基本信息添加
    '''
    form = StudentJiBenMsg()
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
            return redirect(url_for('admin.user_message'))
    return render_template('admin/ge_rens_add.html', form=form)

@admin.route('/student-ji-ben/<student_id>/delete', methods=['GET', 'POST'])
@login_required
def student_geren_delete(student_id):
    '''
    删除基本信息按钮路由
    '''
    geren = Geren.query.filter_by(student_id=student_id).first_or_404()
    db.session.delete(geren)
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('admin.user_message'))


@admin.route('student/<student_id>/show-modify', methods=['GET', 'POST'])
@login_required
def show_or_modify(student_id):
    '''
    查看或修改基本信息
    :param student_id:
    :return:
    '''

    form = StudentJiBenMsgModify()
    geren = Geren.query.filter_by(student_id=student_id).first()
    if form.validate_on_submit():
        if form.modify.data:
            geren.student_id=form.student_id.data
            geren.name=form.name.data
            geren.user_name=form.used_name.data
            geren.sex=form.sex.data
            geren.id_type=form.id_type.data
            geren.id_number=form.id_number.data
            geren.date_of_birth=form.birth_time.data
            geren.min_zu=form.nation.data
            geren.p_status=form.p_status.data
            geren.a_time=form.ad_time.data
            geren.birthplace=form.b_place.data
            geren.a_location=form.acc_location.data
            geren.s_source=form.stu_source.data
            geren.place_of_birth=form.bir_address.data
            db.session.commit()
            flash('修改成功！')
            return redirect(url_for('admin.user_message'))
    form.student_id.data = geren.student_id
    form.name.data = geren.name
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
    form.stu_source.data = geren.s_source
    form.bir_address.data = geren.place_of_birth
    return render_template('admin/ge_rens_modify.html', form=form, user=geren)



"""
学籍信息
"""
@admin.route('/xueji', methods=['GET','POST'])
@login_required
def xue_ji_show():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Xueji.query.paginate(page=page, per_page=per_page)
    student_xue_jis = pagination.items
    contxt = {
        'pagination': pagination,
        'student_xue_jis': student_xue_jis
    }
    form = SearchForm()
    if form.validate_on_submit() and form.info_data.data:
        filters = {or_(Xueji.student_id == form.info_data.data.strip(),
                       Xueji.name == form.info_data.data.strip())}
        pagination = Xueji.query.filter(*filters).paginate(page=page, per_page=per_page)
        student_xue_jis = pagination.items
        contxt = {
            'pagination': pagination,
            'student_xue_jis': student_xue_jis,
        }
        return render_template('admin/xue_ji_show.html', form=form, **contxt)
    return render_template('admin/xue_ji_show.html', form=form,**contxt)

@admin.route('/xueji/add', methods=['GET', 'POST'])
@login_required
def xue_ji_add():
    '''
    学籍添加
    '''
    form = StudentXueJi()
    if form.validate_on_submit():
        if form.ti_jiao.data:
            xue_ji = Xueji(
                name=form.name.data,
                student_id=form.student_id.data,
                school_year=form.school_year.data,
                semester=form.semester.data,
                grade=form.grade.data,
                college_name=form.college_name.data,
                d_name=form.d_name.data,
                p_name=form.p_name.data,
                class_name=form.class_name.data,
                school_system=form.school_system.data,
                xue_ji_zt=form.xue_ji_zt.data,
                zai_xiao=form.zai_xiao.data,
                e_level=form.e_level.data,
                t_method=form.t_method.data,
                student_type=form.student_type.data,
                a_college=form.a_college.data,
                a_profession=form.a_profession.data,
            )
            db.session.add(xue_ji)
            db.session.commit()
            flash('添加成功！')
            return redirect(url_for('admin.xue_ji_show'))
    return render_template('admin/xue_ji_add.html', form=form)

@admin.route('student-xue-ji/<student_id>/show-modify', methods=['GET', 'POST'])
@login_required
def xue_ji_show_or_modify(student_id):
    '''
    查看或修改基本信息
    :param student_id:
    :return:
    '''
    form = StudentXueJiModify()
    xueji = Xueji.query.filter_by(student_id=student_id).first()
    if form.validate_on_submit():
        if form.modify.data:
            xueji.name = form.name.data
            xueji.student_id = form.student_id.data
            xueji.school_year = form.school_year.data
            xueji.semester = form.semester.data
            xueji.grade = form.grade.data
            xueji.college_name = form.college_name.data
            xueji.d_name = form.d_name.data
            xueji.p_name = form.p_name.data
            xueji.class_name = form.class_name.data
            xueji.school_system = form.school_system.data
            xueji.xue_ji_zt = form.xue_ji_zt.data
            xueji.zai_xiao = form.zai_xiao.data
            xueji.e_level = form.e_level.data
            xueji.t_method = form.t_method.data
            xueji.student_type = form.student_type.data
            xueji.a_college = form.a_college.data
            xueji.a_profession = form.a_profession.data
            db.session.commit()
            flash('修改成功！')
            return redirect(url_for('admin.xue_ji_show'))
    form.name.data = xueji.name
    form.student_id.data = xueji.student_id
    form.school_year.data = xueji.school_year
    form.semester.data = xueji.semester
    form.grade.data = xueji.grade
    form.college_name.data = xueji.college_name
    form.d_name.data = xueji.d_name
    form.p_name.data = xueji.p_name
    form.class_name.data = xueji.class_name
    form.school_system.data = xueji.school_system
    form.xue_ji_zt.data = xueji.xue_ji_zt
    form.zai_xiao.data = xueji.zai_xiao
    form.e_level.data = xueji.e_level
    form.t_method.data = xueji.t_method
    form.student_type.data = xueji.student_type
    form.a_college.data = xueji.a_college
    form.a_profession.data = xueji.a_profession
    return render_template('admin/xue_ji_modify.html', form=form, user=xueji)

@admin.route('/student-xue-ji/<student_id>/delete', methods=['GET', 'POST'])
@login_required
def student_xue_ji_delete(student_id):
    '''
    删除基本信息按钮路由
    '''
    xue_ji = Xueji.query.filter_by(student_id=student_id).first_or_404()
    db.session.delete(xue_ji)
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('admin.xue_ji_show'))


"""
成绩信息
"""
@admin.route('/student/score', methods=['GET','POST'])
@login_required
def student_score_show():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Student.query.paginate(page=page, per_page=per_page)
    students = pagination.items
    contxt = {
        'pagination': pagination,
        'students': students
    }
    form = SearchForm()
    if form.validate_on_submit() and form.info_data.data:
        filters = {or_(Student.student_id == form.info_data.data.strip(),
                       Student.name == form.info_data.data.strip())}
        pagination = Student.query.filter(*filters).paginate(page=page, per_page=per_page)
        students = pagination.items
        contxt = {
            'pagination': pagination,
            'students': students,
        }
        return render_template('admin/student_score_show.html', form=form, **contxt)
    return render_template('admin/student_score_show.html', form=form, **contxt)

@admin.route('/student/<student_id>/score/show', methods=['GET','POST'])
@login_required
def student_score_msg(student_id):
    scores = Score.query.filter_by(student_id=student_id).all()
    return render_template('admin/student_score_modify.html', scores=scores)

@admin.route('/student/score/modify', methods=['GET','POST'])
@login_required
def student_modify():
    student_id = request.args.get('student_id')
    course_id = request.args.get('course_id')
    fraction = request.form.get('student_score')
    if fraction:
        sco = Score.query.filter_by(course_id=course_id, student_id=student_id).first()
        sco.fraction = fraction
        db.session.commit()
        flash('更新成功')
    return redirect(url_for('admin.student_score_msg', student_id=student_id))

'''
课程管理
'''
@admin.route('/course/show', methods=['GET','POST'])
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
    if form.validate_on_submit() and form.info_data.data:
        filters = {or_(Course.course_id == form.info_data.data.strip(),
                       Course.course_name == form.info_data.data.strip(),
                       Course.teacher == form.info_data.data.strip(),
                       Course.teacher_id == form.info_data.data.strip()
                       )}
        pagination = Course.query.filter(*filters).paginate(page=page, per_page=per_page)
        courses = pagination.items
        contxt = {
            'pagination': pagination,
            'courses': courses,
        }
        return render_template('admin/course_show.html', form=form, **contxt)
    return render_template("admin/course_show.html", form=form, **contxt)

@admin.route('/course/add', methods=['GET', 'POST'])
@login_required
def add_course():
    '''
    添加课程
    '''
    form = AddCourses()
    course = Course(
        course_id=form.course_id.data,
        course_name=form.course_name.data,
        course_credit=form.course_credit.data,
        teacher_id=form.teacher_id.data,
        teacher=form.teacher_name.data,
        class_room=form.class_room.data,
        course_time=form.course_time.data
    )
    if form.validate_on_submit():
        if form.submit.data:
            db.session.add(course)
            db.session.commit()
            flash('添加课程成功')
            return redirect(url_for('admin.course_show'))
    return render_template('admin/course_add.html', form=form)

@admin.route('/course/<course_id>/modify', methods=['GET', 'POST'])
@login_required
def course_modify(course_id):
    form = ModifyCourses()
    course = Course.query.filter_by(course_id=course_id).first()
    if form.validate_on_submit():
        course.course_id = form.course_id.data
        course.course_name = form.course_name.data
        course.course_credit = form.course_credit.data
        course.teacher_id = form.teacher_id.data
        course.teacher = form.teacher_name.data
        course.class_room = form.class_room.data
        course.course_time = form.course_time.data
        db.session.commit()
        return redirect(url_for('admin.course_show'))
    form.course_id.data = course.course_id
    form.course_name.data = course.course_name
    form.course_credit.data = course.course_credit
    form.teacher_id.data = course.teacher_id
    form.teacher_name.data = course.teacher
    form.class_room.data = course.class_room
    form.course_time.data = course.course_time
    return render_template('admin/course_modify.html', form=form)

@admin.route('/course/<course_id>/delete')
@login_required
def course_delete(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        db.session.delete(course)
        db.session.commit()
        flash('删除成功')
        return redirect(url_for('admin.course_show'))


"""
修改密码(公共本分)
"""
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
            return redirect(url_for('admin.change_password'))
        else:
            flash('原密码不正确')
    return render_template("admin/change_password.html", form=form)

"""
修改邮箱(公共部分)
"""
my_redis = MyRedis.connect()
@admin.route('/retrieve-password/send-code')
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

@admin.route('/change/email', methods=['GET', 'POST'])
@login_required
def change_email():
    email_form = ChangeEmailForm()
    user = User.query.filter_by(email=email_form.old_email.data).first()
    if email_form.validate_on_submit() and \
            MyRedis.get_cache_data(my_redis, email_form.old_email.data) == email_form.verify_code.data:
        user.email = email_form.new_email.data
        db.session.commit()
        flash('修改成功')
    return render_template("admin/change_email.html", form=email_form)

@admin.route('/<student_id>/score/data/downloads')
@login_required
def score_data_download(student_id):
    class Echo(object):
        '''
        只实现类文件接口的写方法的对象。
        '''
        def write(self, value):
            '''
            通过返回值来写入值，而不是存储在缓冲区中
            :param value:
            :return:
            '''
            return value

    writer = csv.writer(Echo())
    def get_data():
        student_scores = Score.query.filter_by(student_id=student_id).all()
        titles =  ['课程编号' , '学号' , '课程名字' , "学分" , '成绩' ]
        header = [codecs.BOM_UTF8.decode("utf8")+codecs.BOM_UTF8.decode()+head for head in titles]
        yield writer.writerow(header)
        for item in student_scores:
            b = [item.course_id , item.student_id , item.course_name , item.course_credit , str(item.fraction)]
            yield writer.writerow(b)
    response = Response(stream_with_context(get_data()))
    response.headers['Content-Disposition'] = "attachment;filename*=UTF-8''{}.csv".format(student_id)
    response.headers['Content-Type'] = 'text/csv;charset=UTF-8'
    return response