from flask import Flask
from .routes import register_routes
from .auth import init_login  # we'll flesh this out later

def create_app():
    app = Flask(__name__)
    # in app/__init__.py, inside create_app() *before* init_login(app):
    app.config.from_mapping(
        SECRET_KEY="…",
        ADMIN_ID=1,
        ADMIN_USERNAME="admin",
        ADMIN_PASSWORD="password",

    )


    # initialize login manager
    init_login(app)

    # register all routes
    register_routes(app)

    return app
