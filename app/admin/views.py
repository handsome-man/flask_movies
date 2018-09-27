# -*- coding: utf-8 -*-
from functools import wraps

from . import admin
from flask import Flask, render_template, redirect, url_for
from app.admin.forms import LoginForm
from app.models import Admin
from flask import flash, session, request


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


# 登录
@admin.route('/login', methods=["GET", "POST"])
@admin_login_req
def login():
    login_form = LoginForm()
    # 提交时验证
    if login_form.validate_on_submit():
        # 获取表单数据
        data = login_form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        # 密码不正确
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误！")
            return redirect(url_for("admin.login"))
        # 密码正确
        session["admin"] = data["account"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template('admin/login.html', form=login_form)


# 退出
@admin.route("/logout")
@admin_login_req
def logout():
    session.pop("account", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route('/pwd')
@admin_login_req
def pwd():
    return render_template('admin/pwd.html')


# 添加标签
@admin.route('/tag_add')
@admin_login_req
def tag_add():
    return render_template('admin/tag_add.html')


# 标签列表
@admin.route('/tag_list')
@admin_login_req
def tag_list():
    return render_template('admin/tag_list.html')


# 添加电影
@admin.route('/movie_add')
@admin_login_req
def movie_add():
    return render_template('admin/movie_add.html')


# 电影列表
@admin.route('/movie_list')
@admin_login_req
def movie_list():
    return render_template('admin/movie_list.html')


# 添加预告
@admin.route('/preview_add')
@admin_login_req
def preview_add():
    return render_template('admin/preview_add.html')


# 预告列表
@admin.route('/preview_list')
@admin_login_req
def preview_list():
    return render_template('admin/preview_list.html')


# 会员列表
@admin.route('/user_list')
@admin_login_req
def user_list():
    return render_template('admin/user_list.html')


# 评论列表
@admin.route('/comment_list')
@admin_login_req
def comment_list():
    return render_template('admin/comment_list.html')


# 收藏列表
@admin.route('/moviecol_list')
@admin_login_req
def moviecol_list():
    return render_template('admin/moviecol_list.html')


# 操作日志列表
@admin.route('/oplog_list')
@admin_login_req
def oplog_list():
    return render_template('admin/oplog_list.html')


# 管理员登录日志列表
@admin.route('/adminloginlog_list')
@admin_login_req
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


# 会员登录日志列表
@admin.route('/userloginlog_list')
@admin_login_req
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


# 添加权限
@admin.route('/auth_add')
@admin_login_req
def auth_add():
    return render_template('admin/auth_add.html')


# 权限列表
@admin.route('/auth_list')
@admin_login_req
def auth_list():
    return render_template('admin/auth_list.html')


# 添加角色
@admin.route('/role_add')
@admin_login_req
def role_add():
    return render_template('admin/role_add.html')


# 角色列表
@admin.route('/role_list')
@admin_login_req
def role_list():
    return render_template('admin/role_list.html')


# 添加管理员
@admin.route('/admin_add')
@admin_login_req
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin.route('/admin_list')
@admin_login_req
def admin_list():
    return render_template('admin/admin_list.html')
