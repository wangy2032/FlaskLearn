# -*- coding: utf-8 -*-
'''
创建管理员蓝本
'''
from flask import Blueprint
admin = Blueprint('admin', __name__)
from . import views