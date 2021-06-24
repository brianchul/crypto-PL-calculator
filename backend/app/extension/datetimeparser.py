from datetime import datetime


def datetimeIsoFormatCleanup(isoFormat):
    return isoFormat[:-1]+".000000"+"+00:00"

def getNowWithFormat():
    return datetime.now().timestamp()
    #return  datetime.now().isoformat(timespec="seconds", sep=" ")