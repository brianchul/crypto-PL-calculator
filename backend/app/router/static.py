from flask import Blueprint, send_from_directory
from ..middleware.response import successResponse
import os


staticBlueprint = Blueprint('web', __name__,static_url_path='', static_folder="build")

@staticBlueprint.route('/')
def index():
    return send_from_directory(staticBlueprint.static_folder, "index.html")
