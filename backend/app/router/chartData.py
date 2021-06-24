from ..controller.chart import queryPrice
from flask import Blueprint, request, current_app
from ..middleware.response import successResponse
import json


chartDataBlueprint = Blueprint('chart', __name__)

@chartDataBlueprint.route("/",methods=["POST"])
def queryAddress():
    r = queryPrice(**request.get_json())

    return successResponse(r)

@chartDataBlueprint.route("/test", methods={"GET"})
def queryTest():
    content = []
    with open("chart.json", "r") as f:
        
        content = json.loads(f.read())
        f.close()
    return successResponse(content)

@chartDataBlueprint.route("/chartPair", methods={"GET"})
def getpairs():
    content = []
    with open("chart.json", "r") as f:
        
        content = json.loads(f.read())
        f.close()
    return successResponse(content)
