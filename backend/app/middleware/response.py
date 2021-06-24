from ..extension.datetimeparser import getNowWithFormat
from datetime import datetime
import json

def successResponse(data):
    try:
        data = json.loads(data)
    except:
        pass
    return {
    "data": data,
    "code": 200,
    "description": None,
    "msg": None,
    "timestamp": getNowWithFormat(),
}
