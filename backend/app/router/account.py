from flask import Blueprint, Response
from ..controller.address import analysisToken


accountBlueprint = Blueprint('account', __name__)

@accountBlueprint.route("/")
def accountIndex():
    return ""

@accountBlueprint.route("/<address>/")
def queryAddress(address):
    query = analysisToken(address)
    return Response(query, 200)

