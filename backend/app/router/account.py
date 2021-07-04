from ..middleware.cache import getOrSetCache
from flask import Blueprint, Response, abort
import json
from ..controller.address import analysisToken
from ..middleware.response import successResponse


accountBlueprint = Blueprint('account', __name__)

@accountBlueprint.route("/test")
def accountIndex():
    content = []
    with open("transaction.json", "r") as f:
        content = json.loads(f.read())
        f.close()
    return successResponse(content)

@accountBlueprint.route("/empty")
def accountEmpty():
    abort(404)
    return 

@accountBlueprint.route("/<address>/")
def queryAddress(address):
    data = analysisToken(address)
    return successResponse(data)

