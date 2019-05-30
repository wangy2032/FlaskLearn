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
    birth_time = DateField('出生时间', validators=[DataRequired()])
    b_place = StringField('籍贯', validators=[DataRequired()])
    acc_location = StringField('户口所在地', validators=[DataRequired()])
    stu_source = StringField('生源地', validators=[DataRequired()])
    bir_address = StringField('出生地', validators=[DataRequired()])
    ad_time = DateField('入学时间', validators=[DataRequired()])
    ti_jiao = SubmitField('提交')
    chong_zhi =SubmitField('重置')