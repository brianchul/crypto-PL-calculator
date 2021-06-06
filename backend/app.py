from flask import Flask, request
from flask.helpers import url_for
from .router.account import accountBlueprint



app = Flask(__name__)



app.register_blueprint(accountBlueprint, url_prefix="/account")

with app.test_request_context('/', method="get"):
    assert request.path == "/"

app.run()