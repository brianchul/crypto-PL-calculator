# tokenA -> Wrapped UST / BUSD-T / WBNB -> tokenB

import requests


class Price():
    def __init__(self) -> None:
        pass

    def getBinancePriceOneMinute(self, symbol, startTime):
        if "USD" not in symbol:
            symbol += "USDT"
        
        url = "https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&startTime={startTime}".format(symbol=symbol)
        url += "?symbol="
        r = requests.get("https://api.binance.com/api/v3/klines")

    def checkSymbol(self, symbol):
        pass
