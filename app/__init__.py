# -*- coding: utf-8 -*-

import pymysql
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 令牌
app.config['SECRET_KEY'] = 'ec0eba98fb9d472b95ce240b7ee8f4e2'

# 配置flask配置对象中键：SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:liulunan@127.0.0.1:3306/movies"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
db = SQLAlchemy(app)

from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
