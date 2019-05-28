# -*- coding: utf-8 -*-
'''
创建管理员蓝本
'''
from flask import Blueprint
student = Blueprint('student', __name__)
from . import views
