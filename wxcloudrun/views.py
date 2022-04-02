from datetime import datetime
from flask import render_template, request, Flask
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import numpy as np
import cv2
import base64
import os
import json
from WeJRcount import JRcount
from Wepushup import pushup
from Wepullup import pullup

def jumprpoe_count(video):
    tmp = JRcount(video)
    return tmp

def pushup_count(video):
    tmp = pushup(video)
    return tmp

def pullup_count(video):
    tmp = pullup(video)
    return tmp

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')

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

@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
