from flask import Blueprint

print('/app/main/__init__.py')

bp = Blueprint('main', __name__)

from app.main import routes  # noqa: E402
