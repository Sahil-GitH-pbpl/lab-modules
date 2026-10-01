from flask import Flask

from .config import Config
from .routes import bp
from .schema import ensure_equipment_tables


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)
    app.register_blueprint(bp)
    with app.app_context():
        ensure_equipment_tables()
    return app
