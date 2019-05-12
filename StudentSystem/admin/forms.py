# -*- coding: utf-8 -*-
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm

'''
搜索表单
'''
class SearchForm(FlaskForm):
    info_data = StringField()
    search = SubmitField('搜索')

'''
账户添加表单
'''
class ModifyUserForm(FlaskForm):
    id = StringField('工号')
    username = StringField('姓名')
    email = SubmitField('邮箱')
    password = PasswordField('修改密码')
    submit = SubmitField('修改')
