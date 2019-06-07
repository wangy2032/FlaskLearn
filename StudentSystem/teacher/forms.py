# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField, DateTimeField, DateField,\
    SelectField, BooleanField, SubmitField, ValidationError, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo

'''
学生基本信息表单
'''
class StudentJiBenMsg(FlaskForm):
    student_id = StringField('学号', validators=[DataRequired()])
    name = StringField('姓名', validators=[DataRequired()])
    used_name = StringField('曾用名')
    p_status = SelectField('政治面貌',
                           choices=[('党员', '党员'), ('共青团员', '共青团员'),('群众', '群众')],
                           validators=[DataRequired()])
    sex = SelectField('性别', choices=[('男', '男'), ('女', '女')],
                      validators=[DataRequired()])
    nation = StringField('民族', validators=[DataRequired()])
    id_type = SelectField('证件类型', choices=[('二代身份证', '二代身份证')], validators=[DataRequired()])
    id_number = StringField('证件号码', validators=[DataRequired()])
    birth_time = StringField('出生时间', validators=[DataRequired()])
    b_place = StringField('籍贯', validators=[DataRequired()])
    acc_location = StringField('户口所在地', validators=[DataRequired()])
    stu_source = StringField('生源地', validators=[DataRequired()])
    bir_address = StringField('出生地', validators=[DataRequired()])
    ad_time = StringField('入学时间', validators=[DataRequired()])
    ti_jiao = SubmitField('提交')
    chong_zhi =SubmitField('重置')
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
    grade = StringField('年级', validators=[DataRequired()])
    college_name = StringField('学院名称', validators=[DataRequired()])
    d_name = StringField('系名称', validators=[DataRequired()])
    p_name = StringField('专业名称', validators=[DataRequired()])
    class_name = StringField('班级名字', validators=[DataRequired()])
    school_system = StringField('学制', validators=[DataRequired()])
    xue_ji_zt = SelectField('学籍状态', choices=[('注册', '注册'),
                                          ('没有注册', '没有注册')])
    zai_xiao = SelectField('是否在校', choices=[('是', '是'),
                                          ('否', '否')])
    e_level = SelectField('学历层次', choices=[('专科', '专科'),
                                          ('本科', '本科'),
                                           ('硕士', '硕士'),
                                           ('博士', '博士')])
    t_method = StringField('培养方式', validators=[DataRequired()])
    student_type = StringField('学生类型', validators=[DataRequired()])
    a_college = StringField('招生学院', validators=[DataRequired()])
    a_profession = StringField('招生专业', validators=[DataRequired()])
    ti_jiao = SubmitField('提交')
    chong_zhi = SubmitField('重置')
    modify = SubmitField('修改')

'''
搜索表单
'''
class SearchForm(FlaskForm):
    search = StringField('条件', validators=[DataRequired()])
    submit = SubmitField('搜索')