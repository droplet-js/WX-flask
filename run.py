# 创建应用实例
import sys
import numpy as np
import cv2
import base64
import os
import json
from flask import Flask
from flask import request
import os
from WeJRcount import JRcount
from Wepushup import pushup
from Wepullup import pullup
from wxcloudrun import app


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

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
