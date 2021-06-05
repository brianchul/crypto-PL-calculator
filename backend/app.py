from flask import Flask, request
from flask.helpers import url_for


app = Flask(__name__)



app.register_blueprint()

with app.test_request_context('/', method="get"):
    assert request.path == "/"

app.run()