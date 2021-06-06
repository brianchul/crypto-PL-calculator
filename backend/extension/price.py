# tokenA -> Wrapped UST / BUSD-T / WBNB -> tokenB

import requests
from datetime import datetime, timedelta
import json


class Price():
    def __init__(self) -> None:
        self.binanceApiUrl = "https://api.binance.com/api/v3/klines"
        pass

    def getBinancePriceOneMinute(self, symbol, startTime):
        if "USD" not in symbol:
            symbol += "USDT"

        url = "https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&startTime={startTime}".format(symbol=symbol)
        url += "?symbol="
        r = requests.get("https://api.binance.com/api/v3/klines")

    def checkSymbol(self, symbol):
        pass

    def getBNBprice(self, startTime: datetime):
        endTime = startTime + timedelta(minutes=1)
        parameters = {
            "symbol": "BNBUSDT",
            "interval": "1m",
            "startTime": self.bnbApiTimestampFormat(startTime),
            "endTime": self.bnbApiTimestampFormat(endTime)
        }
        response = requests.get(self.binanceApiUrl, params=parameters)
        if response.text == "":
            return 0
        price = float(json.loads(response.text)[0][1])
        return price

    def bnbApiTimestampFormat(self, dt: datetime):
        timestamp = dt.timestamp()
        timestamp = timestamp * 1000
        return int(timestamp)

