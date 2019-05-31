# -*- coding: utf-8 -*-
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread
from . import mail


'''
邮件发送功能
'''
#发送异步电子邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

#发送邮件
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    #邮箱主题subject
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASK_MAIL_SENDER'], recipients=[to])
    #邮件内容会以txt和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr