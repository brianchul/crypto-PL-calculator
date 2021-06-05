from flask import Blueprint, Response


accountBlueprint = Blueprint('account', __name__)

@accountBlueprint.route("/")
def accountIndex():
    return ""

@accountBlueprint.route("/<address>")
def queryAddress(address):
    
    return Response("", 200)

