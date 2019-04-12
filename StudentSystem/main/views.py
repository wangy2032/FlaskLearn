# -*- coding: utf-8 -*-

from . import  main
from flask import redirect, url_for, render_template

@main.route('/', methods=['GET', 'POST'])
def index():
    return  render_template('index.html')

@main.route('/base')
def base():
    return render_template('base1.html')