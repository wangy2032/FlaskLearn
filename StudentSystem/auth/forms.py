# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField, BooleanField, SubmitField, ValidationError, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User


'''
登陆表单
'''
class LoginForm(FlaskForm):
    StudentId = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


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
账户表单
'''
class AddUserForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired()])
    student_id = StringField('学号', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])
    role = RadioField('身份', choices=[('学生', '学生'), ('教师', '教师')], default='学生')
    submit = SubmitField('添加账户')

'''
添加学生信息表单
'''
class AddStudentForm(FlaskForm):
    stu_id = StringField("学生学号", validators=[DataRequired(message="这能空?"), Length(6, 15, "有点短?有点长?")])
    name = StringField("学生姓名", validators=[DataRequired(message="这能空?"), Length(-1, 10, "名字过长")])
    cls = StringField("专业班级", validators=[DataRequired(message="没有数据不好交差"), Length(-1, 15, "精简一下")])
    addr = StringField("所在寝室", validators=[DataRequired(message="没有数据不好交差"), Length(-1, 15, "字太多了")])
    phone = StringField("联系方式", validators=[DataRequired(message="没有数据不好交差")])
    add = SubmitField("提交")

'''
搜索表单
'''
class SearchForm(FlaskForm):
    student_number = StringField('学号')
    ti_jiao = SubmitField('提交')

'''
找回密码表单
'''
class RetrievePasswordForm(FlaskForm):

    email = StringField("注册时邮箱", validators=[DataRequired(message='邮箱不能为空'),
                                             Email(message='邮箱格式不正确?')])
    password = PasswordField("密码", validators=[DataRequired(message='密码不能为空'),
                                               Length(6, message='密码长度不得小于6位数')])
    confirm = PasswordField("确认密码", validators=[DataRequired(message='密码不能为空'),
                                                EqualTo('password', "两次密码不一致")])
    submit = SubmitField("确认")