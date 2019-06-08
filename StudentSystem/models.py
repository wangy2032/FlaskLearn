# -*- coding: utf-8 -*-

from . import db
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
'''
用户表
'''
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128))
    create_time = db.Column(db.DateTime(), default=datetime.now())
    new_login_time = db.Column(db.DateTime(), default=datetime.now())
    login_number = db.Column(db.Integer(), default=0)

    @property
    def password(self):
        raise AttributeError('为了安全密码无法获得')
    #用于计算密码的hash值
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    #用于校验输入的密码和数据库你的密码是否相等
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# 用户加载函数
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

'''
学生老师中间表
'''

student_teacher_table = db.Table(
    'student_teach',
    db.Column('student_id', db.String(64), db.ForeignKey('students.student_id')),
    db.Column('teacher_id', db.String(64), db.ForeignKey('teachers.teacher_id'))
)
'''
课程
'''
class Course(db.Model):
    __tablename__='courses'
    course_id = db.Column(db.String(64), primary_key=True)#课程编号
    course_name = db.Column(db.String(64))#课程编号
    course_credit = db.Column(db.String(64))#课程编号
    teacher_id = db.Column(db.String(64),db.ForeignKey('teachers.teacher_id'))    #老师工号
    teacher = db.Column(db.String(64))    #老师名字
    class_room = db.Column(db.String(64))    #上课教室
    course_time = db.Column(db.String(64))    #课时

'''
学生表
'''
class Student(db.Model):
    __tablename__='students'
    student_id = db.Column(db.String(64),primary_key=True)
    name = db.Column(db.String(64))
    ji_ben_msg = db.relationship('Geren', uselist=False)
    xue_ji_msg = db.relationship('Xueji', uselist=False)
    teachers = db.relationship('Teacher',
                               secondary=student_teacher_table,
                               back_populates='students')

'''
老师表
'''
class Teacher(db.Model):
    __tablename__='teachers'
    teacher_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    course_msg = db.relationship('Course', uselist=False)
    students = db.relationship('Student',
                               secondary=student_teacher_table,
                               back_populates='teachers')


'''
基本信息表
'''
class Geren(db.Model):
    __tablename__ = 'gerens'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(64),  #学号
                           db.ForeignKey('students.student_id'))
    name = db.Column(db.String(64))#姓名
    user_name = db.Column(db.String(64))#曾用名
    sex = db.Column(db.String(64))    #性别
    id_type = db.Column(db.String(64)) #证件类型
    id_number = db.Column(db.String(64),unique=True)#证件号码
    date_of_birth = db.Column(db.String(64))#出生年月
    min_zu = db.Column(db.String(64))   #民族
    p_status= db.Column(db.String(64))    #政治面貌
    a_time = db.Column(db.String(64))    #入学时间
    birthplace = db.Column(db.String(64))    #籍贯
    a_location = db.Column(db.String(64))    #户口所在地
    s_source= db.Column(db.String(64))    #生源地
    place_of_birth= db.Column(db.String(64))    #出生地
    user_image = db.Column(db.String(128))  #张片

'''
学籍信息表
'''
class Xueji(db.Model):
    __tablename__ = 'xuejis'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) #姓名
    student_id = db.Column(db.String(64) ,db.ForeignKey('students.student_id'))
    school_year= db.Column(db.String(64))    #学年
    semester = db.Column(db.String(64))    #学期
    grade = db.Column(db.String(64))    #年级
    college_name = db.Column(db.String(64))    #学院名称
    d_name = db.Column(db.String(64))    #系名称
    p_name = db.Column(db.String(64))    #专业名字
    class_name = db.Column(db.String(64))    #班级名字
    school_system = db.Column(db.String(64))    #学制
    xue_ji_zt = db.Column(db.String(64))    #学籍状态
    zai_xiao= db.Column(db.String(64))    #是否在校
    e_level= db.Column(db.String(64))    #学历层次
    t_method= db.Column(db.String(64))    #培养方式
    student_type = db.Column(db.String(64))    #学生类型
    a_college= db.Column(db.String(64))    #招生学院
    a_profession= db.Column(db.String(64))    #招生专业

'''
成绩信息表
'''




