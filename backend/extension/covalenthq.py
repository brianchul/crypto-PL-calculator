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

    async def fetch(self, session, url):
        sleepTime = random.randint(0,10)/10
        time.sleep(sleepTime)
        async with session.get(url) as response:
            return await response.text()

    async def getTransactionLogs(self, transactionIDs):

        tasks = []
        async with aiohttp.ClientSession(auth=BasicAuth(self.covalentApiKey, "")) as session:
            for txid in transactionIDs:
                transactionPrefix = self.covalentOneTransactionPrefix.format(transactionID=txid)
                url = self.covalentApiUrl.format(prefix=transactionPrefix)
                tasks.append(self.fetch(session, url))
            fetched = await asyncio.gather(*tasks)

        return fetched