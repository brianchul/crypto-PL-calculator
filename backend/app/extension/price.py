# tokenA -> Wrapped UST / BUSD-T / WBNB -> tokenB

import asyncio
import aiohttp
from .requestFetch import SessionFetch
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



    async def getBNBprice(self, startTime: datetime):
        Fetch = SessionFetch()
        endTime = startTime + timedelta(minutes=1)
        parameters = {
            "symbol": "BNBUSDT",
            "interval": "1m",
            "startTime": self.bnbApiTimestampFormat(startTime),
            "endTime": self.bnbApiTimestampFormat(endTime)
        }
        task = []
        async with aiohttp.ClientSession() as session:
            task.append(Fetch.fetch(session, self.binanceApiUrl, param=parameters))
            fetched = await asyncio.gather(*task)

            return float(json.loads(fetched[0])[0][1])


    def bnbApiTimestampFormat(self, dt: datetime):
        timestamp = dt.timestamp()
        timestamp = timestamp * 1000
        return int(timestamp)

