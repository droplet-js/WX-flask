from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import config
import numpy as np
import cv2
import base64
import os
import json
from WeJRcount import JRcount
from Wepushup import pushup
from Wepullup import pullup

# 因MySQLDB不支持Python3，使用pymysql扩展库代替MySQLDB库
pymysql.install_as_MySQLdb()

# 初始化web应用
app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = config.DEBUG

# 设定数据库链接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/flask_demo'.format(config.username, config.password,
                                                                             config.db_address)

# 初始化DB操作对象
db = SQLAlchemy(app)

# 加载控制器
from wxcloudrun import views

# 加载配置
app.config.from_object('config')


app = Flask(__name__)

def jumprpoe_count(video):
    tmp = JRcount(video)
    return tmp

def pushup_count(video):
    tmp = pushup(video)
    return tmp

def pullup_count(video):
    tmp = pullup(video)
    return tmp

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/uploadvid", methods=["POST"])
def get_upload_video():
    print(request)
    up_video = base64.b64decode(request.form.get("video"))  #base64进行解码还原。    
    with open("1.mp4","wb") as f:                           #存入，存入地址为服务器中的项目地址。
         f.write(up_video) 

    type = request.form.get("info")
    print(type)
    tep=[]
    if type == 'jump rope':
        tep = jumprpoe_count("1.mp4")

    if type == 'push ups':
        tep = pushup_count("1.mp4")

    if type == 'pull ups':
        tep = pullup_count("1.mp4")

    os.remove("1.mp4")
    print(tep)
    
    return dict(date=str(tep[0]), type=str(tep[1]), count=str(tep[2]))
