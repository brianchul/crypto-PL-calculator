import os
from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS
from config import config
import logging
from logging.handlers import TimedRotatingFileHandler
from .middleware.errorHandler import register_errors


def create_app(config_name):
    app = Flask(__name__,static_url_path='', static_folder="../../frontend/app/build")

    CORS(app)

    app.config.from_object(config[config_name])


    #register_logging(app)
    register_errors(app)

    from .router.account import accountBlueprint
    app.register_blueprint(accountBlueprint, url_prefix="/account")

    from .router.chartData import chartDataBlueprint
    app.register_blueprint(chartDataBlueprint, url_prefix="/chart")

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, "index.html")

    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    return app

    with app.test_request_context('/', method="get"):
        assert request.path == "/"


def register_logging(app):
    app.logger.name = 'app'

    # socket_handler
    socketHandler = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    app.logger.addHandler(socketHandler)

    """
    # set own root logger
    rootLogger = logging.getLogger(__name__)
    rootLogger.setLevel(logging.DEBUG)
    socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    rootLogger.addHandler(socketHandler)
    rootLogger.setLevel(logging.DEBUG)
    """