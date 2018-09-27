# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="账号",  # 字段名称
        # 账号不能为空
        validators=[
            DataRequired("请输入账号！")
        ],
        # 描述
        description="账号",
        # 附加选项，前端页面上除了name和type，其它属性都要加上
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号",
            # "required": "required",
        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
            # "required": "required",
        }
    )

    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        # 统计admin条数
        admin = Admin.query.filter_by(name=account).count()
        # 判断是否有条数
        if admin == 0:
            raise ValidationError("账号不存在")