# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import  StringField,PasswordField, BooleanField, \
    SubmitField, ValidationError, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from StudentSystem import file

"""
选课表单
"""
class CourseAddForm(FlaskForm):
    course_submit = SubmitField('提交')


'''
密码修改
'''
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
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
搜索表单
'''
class SearchForm(FlaskForm):
    info_data = StringField()
    search = SubmitField('搜索')

"""
图片上传表单
"""
class ImageUploadForm(FlaskForm):
    images = FileField('照片选择', validators=[FileRequired('请选择文件'), FileAllowed(file)])
    submit = SubmitField('上传')