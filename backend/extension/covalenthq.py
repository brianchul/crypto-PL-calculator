import asyncio
import aiohttp
from aiohttp.helpers import BasicAuth
import requests
from requests.models import HTTPBasicAuth
import json
import configparser
import time
import random


class Convalenthq():
    MAX_RETRY = 10
    def __init__(self) -> None:
        self.address = ""
        self.transaction = ""
        self.covalentApiUrl = "https://api.covalenthq.com/v1/56/{prefix}"
        self.covalentOneTransactionPrefix = "transaction_v2/{transactionID}/"
        self.covalentAddressTransactionsPrefix = "address/{address}/transactions_v2/?page-size=9999&block-signed-at-asc=false"
        config =configparser.ConfigParser()
        config.read("config.ini")
        self.covalentApiKey = config["DEFAULT"]["covalentApiKey"]

        pass

    def getAddressTransactions(self, address):
        addressUrl = self.covalentAddressTransactionsPrefix.format(address=address)
        response = requests.get(self.covalentApiUrl.format(prefix=addressUrl), auth=HTTPBasicAuth(self.covalentApiKey, ""))
        return json.loads(response.text), response.status_code

    async def fetch(self, session: aiohttp.ClientSession, url):
        statusCode = 0
        retryCount = 0
        while statusCode != 200 or retryCount > self.MAX_RETRY:
            async with session.get(url) as response:
                statusCode = response.status
                if statusCode == 200:
                    responseText = await response.text()
                    return responseText
            sleepTime = random.randint(10,100)/100
            print("rate limited: count {c}, wait for {t} second to retry".format(c=retryCount, t=sleepTime))
            time.sleep(sleepTime)
            retryCount += 1
        return ""

    async def getTransactionLogs(self, transactionIDs):

        tasks = []
        async with aiohttp.ClientSession(auth=BasicAuth(self.covalentApiKey, "")) as session:
            for txid in transactionIDs:
                transactionPrefix = self.covalentOneTransactionPrefix.format(transactionID=txid)
                url = self.covalentApiUrl.format(prefix=transactionPrefix)
                tasks.append(self.fetch(session, url))
            fetched = await asyncio.gather(*tasks)

        return fetched