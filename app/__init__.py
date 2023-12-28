from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_socketio import SocketIO


db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
socket = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    socket.init_app(app, async_mode=None, logger=False, engine_logger=False)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models  # noqa: E402
