from flask import Flask, request, jsonify
from flask import render_template
from flask import redirect, render_template, session, send_file, send_from_directory
from functools import wraps
import json
import mysql
import time
import os
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = "yangning"  # os.urandom(24)设置一个随机24位字符串为加密盐
app.config.update(TEMPLATE_AUTO_RELOAD=True)


def wrapper(func):
    @wraps(func)  # 保存原来函数的所有属性,包括文件名
    def inner(*args, **kwargs):
        # 校验session
        if session.get("user"):
            ret = func(*args, **kwargs)  # func = home
            return ret
        else:
            return redirect("/admin")
    return inner


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('login.html')
    t_id = request.form['t_id']
    password = request.form['password']
    s = mysql.Sql()
    r = s.search('''
        SELECT * FROM ADMIN WHERE username='%s' and password='%s'
    ''' % (t_id, password))
    if(len(r) == 0):
        return "账号或密码错误"
    else:
        session["user"] = r[0]
        # 接入管理员端
        return "success"


@app.route('/index', methods=['GET', 'POST'])
@wrapper
def index():
    if request.method == 'GET':
        return render_template('index.html')
    s = mysql.Sql()
    r = s.search(
        '''
        SELECT * FROM FORM
        '''
    )
    return jsonify(r)


@app.route('/getform', methods=['POST'])
def getform():
    text = request.form['text']
    name = request.form['name']
    phonenumber = request.form['phonenumber']
    email = request.form['email']
    address = request.form['address']
    s = mysql.Sql()
    sql_str = '''
            INSERT INTO form(
                text, name,phonenumber,email,address
                )
            VALUES ("%s", '%s', '%s','%s','%s')
        ''' % (
        text,
        name,
        phonenumber,
        email,
        address
    )
    s.sqlstr(sql_str)
    return "success"


if __name__ == '__main__':
    app.run(debug=True)
