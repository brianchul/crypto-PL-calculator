def datetimeIsoFormatCleanup(isoFormat):
    return isoFormat[:-1]+".000000"+"+00:00"