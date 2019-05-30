# -*- coding: utf-8 -*-

from . import db
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#用户模型
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # confirmed = db.Column(db.Boolean(),default=False)
    confirmed = db.Column(db.String(64), default='否')
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.Column(db.String(128))

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

    # 生成确认令牌
    def getToken(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    #确认令牌
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

# # 用户加载函数
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    #课程编号
    course_id = db.Column(db.String(64), primary_key=True)
    #课程名称
    course_name = db.Column(db.String(64))
    #课程学分
    course_credit = db.Column(db.String(64))
    #老师工号
    teacher_id = db.Column(db.String(64),db.ForeignKey('teachers.teacher_id'))
    #老师名字
    teacher = db.Column(db.String(64))
    #上课教室
    class_room = db.Column(db.String(64))
    #课时
    course_time = db.Column(db.String(64))

class Student(db.Model):
    __tablename__='students'
    student_id = db.Column(db.String(64),primary_key=True)
    name = db.Column(db.String(64))
    ji_ben_msg = db.relationship('Geren', uselist=False)
    xue_ji_msg = db.relationship('Xueji', uselist=False)
    teachers = db.relationship('Teacher',
                               secondary=student_teacher_table,
                               back_populates='students')

class Teacher(db.Model):
    __tablename__='teachers'
    teacher_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    course_msg = db.relationship('Course', uselist=False)
    students = db.relationship('Student',
                               secondary=student_teacher_table,
                               back_populates='teachers')


#个人信息
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

#学籍信息
class Xueji(db.Model):
    __tablename__ = 'xuejis'
    id = db.Column(db.Integer, primary_key=True)
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
成绩信息
'''



