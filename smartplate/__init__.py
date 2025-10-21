from flask import Flask
from .config import Config
from .extensions import db
from .blueprints.api import api_bp
from .blueprints.web import web_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(web_bp)

    return app


