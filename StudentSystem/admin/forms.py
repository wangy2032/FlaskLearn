# -*- coding: utf-8 -*-
from wtforms import StringField, SubmitField, PasswordField, SelectField\
    ,DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from StudentSystem.models import Geren

'''
学生基本信息表单
'''
class StudentJiBenMsg(FlaskForm):
    def validate_student_id(form, field):
        student_id = field.data
        user = Geren.query.filter_by(student_id=student_id).first()
        if user:
            raise ValidationError("昵称已存在")

    student_id = StringField('学号', validators=[DataRequired(), validate_student_id, Length(11, message='长度为11')])
    name = StringField('姓名', validators=[DataRequired()])
    used_name = StringField('曾用名')
    p_status = SelectField('政治面貌',
                           choices=[('党员', '党员'), ('共青团员', '共青团员'),('群众', '群众')],
                           validators=[DataRequired()])
    sex = SelectField('性别', choices=[('男', '男'), ('女', '女')],
                      validators=[DataRequired()])
    nation = StringField('民族', validators=[DataRequired()])
    id_type = SelectField('证件类型', choices=[('二代身份证', '二代身份证')], validators=[DataRequired()])
    id_number = StringField('证件号码', validators=[DataRequired(), Length(18, message='长度18')])
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
    student_id = StringField('学号', validators=[DataRequired()])
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
账户修改表单
'''
class ModifyUserForm(FlaskForm):
    id = StringField('工号')
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
    number = StringField('工号')
    username = StringField('姓名')
    email = StringField('邮箱')
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
    course_id = StringField('课程编号')
    course_name = StringField('课程名字')
    course_credit=StringField('课程学分')
    teacher_id = StringField('老师工号')
    teacher_name = StringField('老师名字')
    class_room = StringField('上课教室')
    course_time = StringField('课程时长')
    submit = SubmitField('提交')