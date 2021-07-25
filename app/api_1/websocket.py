#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@software: PyCharm
@file: flaskWebSocket.py
@time: 2019/2/19 10:20
@describe: flask_sockets 实现websocket
"""
import json
import sys
import os
import time
from flask import Blueprint
from app.extensions import sockets,db
from app.dataBase.models import Devices,Messages
from gevent import monkey
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

rece_bp = Blueprint('receive', __name__)

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
monkey.patch_all()



connect_list = []

@sockets.route('/receive')  # 指定路由
def echo_socket(ws):
    msg_obj = None
    last_update_time = 0
    timeout_count = 0
    while not ws.closed:
        rec = ws.receive()  # 接收到消息
        if rec is not None:
            ws.send(str("Connect server successful!"))
            rec = rec.split('/t').split('/n')
            if "deviceMAC" in rec:
                mac = rec
                dev_obj = Devices.query.filter(Devices.mac==mac).first()
                if dev_obj:
                    connect_list.append({
                        "user_id":dev_obj.user_id,
                        "mac_id":dev_obj.id,
                        "ws":ws,
                        "message_obj":Devices.message
                    })
                    msg = Devices.message
                    msg.connect_time = int(round(time.time() * 1000))
                    msg.connect_count = msg.connect_count + 1
                    db.session.add(msg)
                    db.session.commit()
                    msg_obj = msg

            now_timestamp = int(round(time.time() * 1000))
            msg_obj.current_update_time = now_timestamp
            timeout = now_timestamp - last_update_time
            if timeout > msg_obj.update_interval:
                msg_obj.timeout = timeout
                timeout_count += 1


            """ 如果客户端未发送消息给服务端，就调用接收消息方法，则会导致receive()接收消息为空，关闭此次连接 """
            ws.send(str("Connect server successful!"))
        else:
            msg_obj.disonnect_time = int(round(time.time() * 1000))
            timeout_count = 0

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()

