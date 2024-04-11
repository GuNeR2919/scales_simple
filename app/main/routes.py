from time import sleep
from flask import render_template, url_for, request, current_app
from threading import Thread, Event
from app import socket, scales_daemon, db
from app.main import bp
from app.models import Weight
from datetime import datetime, timezone
import sqlalchemy as sa

print('/app/main/routes.py')

thread = Thread()
thread_stop_event = Event()
clients = 0

print('First thread status is', thread)


def get_weight():
    """
    Send current weight to client with date
    """
    while True:
        if not thread_stop_event.is_set():
            print(f'{datetime.now().strftime("%y.%m.%d.%H:%M:%S")} Client: received weight is {scales_daemon.weight}')
            socket.emit('weight', {'data': scales_daemon.weight})
            sleep(2)
        else:
            continue


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title= current_app.config['SCALES_TITLE'])


@bp.route('/weights', methods=['GET', 'POST'])
def weights():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Weight).where(Weight.weight >= current_app.config['MINIMUM_FILTERED_WEIGHT']).order_by(Weight.mtime.desc())
    records = db.paginate(query, page=page, per_page=current_app.config['WEIGHTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.weights', page=records.next_num) \
        if records.has_next else None
    prev_url = url_for('main.weights', page=records.prev_num) \
        if records.has_prev else None
    for w in records.items:
        w.mtime = datetime.fromtimestamp(w.mtime, tz=timezone.utc)
    return render_template('weights.html', title='Weights list',
                           weights=records.items, next_url=next_url,
                           prev_url=prev_url, pagination=records)


@socket.on('connect')
def test_connect():
    global clients
    global thread
    clients += 1
    ip = request.remote_addr
    print(f'Client %s connected. IP %s' % (clients, ip))
    if not thread.is_alive() and not thread_stop_event.is_set():
        print('Starting client thread')
        thread = socket.start_background_task(get_weight)
    else:
        print('Continue client thread')
        thread_stop_event.clear()


@socket.on('disconnect')
def test_disconnect():
    global clients
    print('Client disconnected')
    clients -= 1
    print('Clients left: %s' % clients)
    if clients == 0:
        print('Pausing client thread')
        thread_stop_event.set()
