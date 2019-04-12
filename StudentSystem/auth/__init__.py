# -*- coding: utf-8 -*-
#创建登陆蓝本
from flask import Blueprint
auth = Blueprint('auth',__name__)
from . import views