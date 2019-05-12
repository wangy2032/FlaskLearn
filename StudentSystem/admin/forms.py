# -*- coding: utf-8 -*-
from wtforms import StringField, SubmitField, PasswordField, SelectField
from flask_wtf import FlaskForm

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
                           choices=[(3, '学生'), (2, '老师'), (1, '管理员')],
                           default=3, coerce=int)
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
                           choices= [(3, '学生'), (2, '老师'), (1, '管理员')],
                           default=3, coerce=int)
    submit = SubmitField('添加')


