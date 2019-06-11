# -*- coding: utf-8 -*-
from wtforms import StringField, SubmitField, PasswordField, SelectField\
    ,DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from StudentSystem.models import Geren, Teacher, db, User, Student, Course, Xueji

'''
学生基本信息表单
'''
class StudentJiBenMsg(FlaskForm):
    def __init__(self):
        super().__init__()
        self.student_id.choices = [(student.student_id, student.student_id) for student in db.session.query(Student).all()]

    def check_id(self, field):
        tmp = Geren.query.filter_by(id_number=field.data).first()
        if tmp:
            raise ValidationError('身份证存在')

    student_id = SelectField('学号')
    name = StringField('姓名', validators=[DataRequired()])
    used_name = StringField('曾用名')
    p_status = SelectField('政治面貌',
                           choices=[('党员', '党员'), ('共青团员', '共青团员'),('群众', '群众')],
                           validators=[DataRequired()])
    sex = SelectField('性别', choices=[('男', '男'), ('女', '女')],
                      validators=[DataRequired()])
    nation = StringField('民族', validators=[DataRequired()])
    id_type = SelectField('证件类型', choices=[('二代身份证', '二代身份证')], validators=[DataRequired()])
    id_number = StringField('证件号码', validators=[DataRequired(),
                                                Length(18, message='长度18'),
                                                check_id])
    birth_time = StringField('出生时间', validators=[DataRequired()])
    b_place = StringField('籍贯', validators=[DataRequired()])
    acc_location = StringField('户口所在地', validators=[DataRequired()])
    stu_source = StringField('生源地', validators=[DataRequired()])
    bir_address = StringField('出生地', validators=[DataRequired()])
    ad_time = StringField('入学时间', validators=[DataRequired()])
    ti_jiao = SubmitField('提交')
    modify = SubmitField('修改')

'''
学生学籍信息表单
'''
class StudentXueJi(FlaskForm):
    def __init__(self):
        super().__init__()
        self.student_id.choices = [(student.student_id, student.student_id) for student in db.session.query(Student).all()]

    def check_xue_ji(form, field):
        xue_ji = Xueji.query.filter_by(student_id=field.data).first()
        if xue_ji:
            raise ValidationError('此学生学籍已存在')

    student_id = SelectField('学号',validators=[check_xue_ji])
    name = StringField('姓名', validators=[DataRequired()])
    school_year = StringField('学年', validators=[DataRequired()])
    semester = SelectField('学期', choices=[('第一学期', '第一学期'),
                                          ('第二学期', '第二学期')])
    grade = SelectField('年级', choices=[('大一', '大一'),
                                          ('大二', '大二'),('大三', '大三'),
                                          ('大四', '大四'),('研一', '研一'),
                                          ('研二', '研二'),('研三','研三')])
    college_name = StringField('学院名称', validators=[DataRequired()])
    d_name = StringField('系名称', validators=[DataRequired()])
    p_name = StringField('专业名称', validators=[DataRequired()])
    class_name = StringField('班级名字', validators=[DataRequired()])
    school_system = SelectField('学制', choices=[('4', '4'),
                                          ('3', '3')])
    xue_ji_zt = SelectField('学籍状态', choices=[('注册', '注册'),
                                          ('没有注册', '没有注册')])
    zai_xiao = SelectField('是否在校', choices=[('是', '是'),
                                          ('否', '否')])
    e_level = SelectField('学历层次', choices=[('专科', '专科'),
                                          ('本科', '本科'),
                                           ('硕士', '硕士'),
                                           ('博士', '博士')])
    t_method = StringField('培养方式', validators=[DataRequired()])
    student_type = SelectField('学生类型', choices=[('专科', '专科'),
                                          ('本科', '本科'),
                                           ('硕士', '硕士'),
                                           ('博士', '博士')])
    a_college = StringField('招生学院', validators=[DataRequired()])
    a_profession = StringField('招生专业', validators=[DataRequired()])
    ti_jiao = SubmitField('提交')
    modify = SubmitField('修改')


'''
搜索表单
'''
class SearchForm(FlaskForm):
    info_data = StringField()
    search = SubmitField('搜索')

'''
成绩表单
'''
class ScoreForm(FlaskForm):
    score = StringField()
    submit = SubmitField()

'''
账户修改表单
'''
class ModifyUserForm(FlaskForm):
    id = StringField('工号或学号')
    username = StringField('姓名')
    email = StringField('邮箱')
    password = PasswordField('修改密码')
    identify = SelectField('身份',
                           choices=[("student", '学生'), ("teacher", '老师'), ("admin", '管理员')],
                           default="学生")
    submit = SubmitField('修改')


'''
添加账户
'''
class AddTeacherForm(FlaskForm):
    def check_user(form, field):
        student_id = field.data
        user = User.query.filter_by(student_id=student_id).first()
        if user:
            raise ValidationError('用户存在')
    def check_email(form, field):
        email = field.data
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError('邮箱已使用')
    number = StringField('工号', validators=[check_user])
    username = StringField('姓名')
    email = StringField('邮箱', validators=[check_email])
    password = StringField('默认密码')
    identity = SelectField('身份',
                           choices= [("student", '学生'), ("teacher", '老师'), ("admin", '管理员')],
                           default="学生")
    submit = SubmitField('添加')

'''
密码修改
'''
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('修改密码')

'''
邮箱修改
'''
class ChangeEmailForm(FlaskForm):
    old_email = StringField('原邮箱', validators=[DataRequired(), Email()])
    new_email = StringField('新邮箱', validators=[DataRequired(), Email()])
    verify_code = StringField('验证码')
    submit = SubmitField('修改邮箱')



'''
添加课程表单
'''
class AddCourses(FlaskForm):
    def __init__(self):
        super().__init__()
        self.teacher_id.choices = [(te.teacher_id, te.teacher_id) for te in db.session.query(Teacher).all()]

    def check_course(form, field):
        course_id = field.data
        course = Course.query.filter_by(course_id=course_id).first()
        if course:
            raise ValidationError('课程存在')
    course_id = StringField('课程编号', validators=[DataRequired(), Length(1,6, message="长度过长"), check_course])
    course_name = StringField('课程名字', validators=[DataRequired()])
    course_credit=StringField('课程学分', validators=[DataRequired(), Length(1,3, message='长度过长')])
    teacher_id = SelectField('老师工号')
    teacher_name = StringField('老师名字')
    class_room = StringField('授课地点', validators=[DataRequired()])
    course_time = StringField('课程时长', validators=[DataRequired()])
    submit = SubmitField('提交')
    modify = SubmitField('修改')

'''
添加课程表单
'''
class ModifyCourses(FlaskForm):
    def __init__(self):
        super().__init__()
        self.teacher_id.choices = [(te.teacher_id, te.teacher_id) for te in db.session.query(Teacher).all()]
    course_id = StringField('课程编号', validators=[DataRequired(), Length(1,6, message="长度过长")])
    course_name = StringField('课程名字', validators=[DataRequired()])
    course_credit=StringField('课程学分', validators=[DataRequired(), Length(1,3, message='长度过长')])
    teacher_id = SelectField('老师工号')
    teacher_name = StringField('老师名字')
    class_room = StringField('授课地点', validators=[DataRequired()])
    course_time = StringField('课程时长', validators=[DataRequired()])
    submit = SubmitField('提交')
    modify = SubmitField('修改')

