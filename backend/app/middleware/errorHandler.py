
from ..extension.datetimeparser import getNowWithFormat
from flask import json
from datetime import datetime

def register_errors(app):
    from werkzeug.exceptions import HTTPException
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "data": None,
            "timestamp": getNowWithFormat(),
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
