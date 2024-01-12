import socket
import re
from time import sleep
from app import db
from threading import Thread
from datetime import datetime
from app.models import Weight
from flask import current_app

weight = 0


def async_start_daemon(app):
    with app.app_context():
        get_weight()


def start_daemon():
    print("Starting")
    th = Thread(target=async_start_daemon, args=(current_app._get_current_object(),))
    th.daemon = True
    th.start()


def close_scales_sock(sc_sock):  # destroy scales socket function
    sc_sock.close()
    wght = 'Connecting to scales...'
    sleep(2)
    print('Daemon: Close socket function call.')
    return False, wght


def newscl_weight(wght):
    wght = re.search(r'^\D*(\d*)kg', wght)
    if wght:
        # if str(wght.group(1)) in ('-', '+'):
        wght = str(wght.group(1))
        return True, wght
    else:
        return False, 0


def get_weight():
    global weight
    time_stamp = 0
    weight_stamp = None
    db_new = True
    scales_con = False
    scales_sock = None
    weight = 'Connecting to scales...'
    try:
        while True:
            if not scales_con:
                try:
                    scales_sock = \
                        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    scales_sock.connect((current_app.config['SCALES_HOST'],
                                         current_app.config['SCALES_PORT']))
                    scales_con = True
                except BaseException as msg:
                    print('Daemon: cant connect to scales -', msg)
                    scales_con = False
                    sleep(10)
            else:
                try:
                    weight_rcv = scales_sock.recv(51).decode('ascii')
                    if not weight_rcv:
                        weight = 'Connecting to the scales ...'
                        scales_con, smwght = close_scales_sock(scales_sock)
                        continue
                    time_cur = int(datetime.now().timestamp())
                    time_pid = int(datetime.now().strftime("%y%m%d%H%M%S"))
                    # print('Daemon: receive -', weight_rcv)
                    smscl, smwght = newscl_weight(weight_rcv)
                    if smscl:
                        weight = smwght
                        if weight_stamp != smwght and weight_stamp != 0:
                            time_stamp = time_cur
                            weight_stamp = smwght
                            db_new = True
                            print('Daemon: time_stamp -', time_pid)
                        else:
                            if time_cur - time_stamp >= 15 and db_new:
                                weight_db = Weight(mtime=time_cur,
                                                   yard='jel1',
                                                   typ='',
                                                   weight=weight_stamp,
                                                   pid=time_pid)
                                db.session.add(weight_db)
                                db.session.commit()
                                db_new = False
                                print('Daemon: record added to DB')
                    else:
                        weight = 0
                except BaseException as msg:
                    print('Daemon: receiving error -', msg)
                    weight = 'Connecting to scales...'
                    close_scales_sock(scales_sock)
                    continue
    except KeyboardInterrupt:
        close_scales_sock(scales_sock)
        print('Exit')
    print('I got end of Daemon function')
