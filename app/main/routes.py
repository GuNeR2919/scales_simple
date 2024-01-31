from asyncio import threads
from time import sleep
from flask import render_template, url_for, request, current_app
from threading import Thread, Event
from app import socket, scales_daemon
from app.main import bp
from app.models import Weight
from datetime import datetime, timezone

print('/app/main/routes.py')
# socketio = SocketIO(current_app._get_current_object(), async_mode=None, logger=False, engine_logger=False)

thread = Thread()
thread_stop_event = Event()
clients = 0

print('First thread status is', thread)


def get_weight():
    """
    Send current weight to client
    """
    while True:
        if not thread_stop_event.is_set():
            print(f'Client: received weight is {scales_daemon.weight}')
            socket.emit('weight', {'data': scales_daemon.weight})
            sleep(2)
        else:
            continue


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    # scales_daemon.start_daemon()
    return render_template('index.html')


@bp.route('/weights', methods=['GET', 'POST'])
def weights():
    page = request.args.get('page', 1, type=int)
    weight = Weight.query.order_by(Weight.mtime.desc()).paginate(page=page,
                                                                 per_page=current_app.config['WEIGHTS_PER_PAGE'],
                                                                 error_out=False)
    next_url = url_for('main.weights', page=weight.next_num) \
        if weight.has_next else None
    prev_url = url_for('main.weights', page=weight.prev_num) \
        if weight.has_prev else None
    for w in weight.items:
        w.mtime = datetime.fromtimestamp(w.mtime, tz=timezone.utc)
    return render_template('weights.html', title='Weights list',
                           weights=weight.items, next_url=next_url,
                           prev_url=prev_url)


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
