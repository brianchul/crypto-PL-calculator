from flask import Flask
from config import config
import logging
from logging.handlers import TimedRotatingFileHandler


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    #register_logging(app)

    from .router.account import accountBlueprint
    app.register_blueprint(accountBlueprint, url_prefix="/account")

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
    print(app.logger.name)

    """
    # set own root logger
    rootLogger = logging.getLogger(__name__)
    rootLogger.setLevel(logging.DEBUG)
    socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    rootLogger.addHandler(socketHandler)
    rootLogger.setLevel(logging.DEBUG)
    """