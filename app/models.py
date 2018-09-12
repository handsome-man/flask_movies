# -*- coding: utf-8 -*-

from datetime import datetime
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#创建flask对象
app = Flask(__name__)

#配置flask配置对象中键：SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:liulunan@127.0.0.1:3306/movies"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
# print(dir(db))
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base(db)

# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(db)
# session = Session()


class User(db.Model):
    """会员"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号
    info = db.Column(db.Text)
    face = db.Column(db.String(255))  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符

    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship("Comment", backref='user')  # 评论外键关系关联
    moviecols = db.relationship("Moviecol", backref='user')  # 电影收藏外键关系关联

    def __repr__(self):
        return "<User %r>" % self.name


class UserLog(db.Model):
    """会员登录日志"""
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))  # 登陆IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登陆时间

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员

    def __repr__(self):
        return "<Userlog %r>" % self.id


class Tag(db.Model):
    """标签"""
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    movies = db.relationship("Movie", backref='tag')  # 电影外键关联

    def __repr__(self):
        return "<Tag %r>" % self.name


class Movie(db.Model):
    """电影"""
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id '))  # 所属标签
    comments = db.relationship("Comment", backref='movie')  # 评论外键关联关系
    moviecols = db.relationship("Moviecol", backref='movie')  # 电影收藏外键关系关联

    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(db.Model):
    """上映预告"""
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


class Comment(db.Model):
    """评论"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户

    def __repr__(self):
        return "<Comment %r>" % self.id


class Moviecol(db.Model):
    """电影收藏"""
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户

    def __repr__(self):
        return "<Moviecol %r>" % self.id


class Auth(db.Model):
    """权限"""
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


class Role(db.Model):
    """角色"""
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name


class Admin(db.Model):
    """管理员"""
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    adminlogs = db.relationship("AdminLog", backref='admin')  # 管理员登陆日志外键关系关联
    oplogs = db.relationship("OpLog", backref='admin')  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name


class AdminLog(db.Model):
    """管理员登录日志"""
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))  # 登陆IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登陆时间

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员

    def __repr__(self):
        return "<Userlog %r>" % self.id


class OpLog(db.Model):
    """操作日志"""
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    ip = db.Column(db.String(100))  # 登陆IP
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登陆时间

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员

    def __repr__(self):
        return "<OpLog %r>" % self.id


# if __name__ == '__main__':
#     db.create_all()
