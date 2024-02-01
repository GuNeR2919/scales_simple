from app import create_app, db, scales_daemon
from app.models import Weight

print('/scales_simple.py')

app = create_app()

with app.app_context():
    scales_daemon.start_daemon()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Weight': Weight}
