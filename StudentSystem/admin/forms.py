# -*- coding: utf-8 -*-
from wtforms import StringField, SubmitField, PasswordField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo

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
                           choices=[("学生", '学生'), ("老师", '老师'), ("管理员", '管理员')],
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
                           choices= [("学生", '学生'), ("老师", '老师'), ("管理员", '管理员')],
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