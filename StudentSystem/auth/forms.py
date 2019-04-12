# -*- coding: utf-8 -*-
from flask import flash
from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User

'''
登陆表单
'''
class LoginForm(FlaskForm):
    StudentId = StringField('StudentID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

'''
注册表单
'''
class RegisteredForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    StudentId = StringField('StudentID', validators=[DataRequired()])
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    #邮箱验证
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            flash('邮箱存在')
            raise ValidationError('邮箱已存在.')
    #学号验证
    def validate_StudentId(self, field):
        if User.query.filter_by(StudentId=field.data).first():
            flash('学号存在')
            raise ValidationError('学号已存在.')


'''
密码修改
'''
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('old PassWord', validators=[DataRequired()])
    password = PasswordField('PassWord', validators=[DataRequired(), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')