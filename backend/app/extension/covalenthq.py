import asyncio
import aiohttp
from aiohttp.helpers import BasicAuth
import requests
from requests.models import HTTPBasicAuth
import json
from flask import current_app


from ..extension.requestFetch import SessionFetch


class Convalenthq():
    def __init__(self) -> None:
        self.address = ""
        self.transaction = ""
        self.covalentApiUrl = "https://api.covalenthq.com/v1/56/{prefix}"
        self.covalentOneTransactionPrefix = "transaction_v2/{transactionID}/"
        self.covalentAddressTransactionsPrefix = "address/{address}/transactions_v2/?page-size=200&block-signed-at-asc=false"
        self.covalentAddressBalancePrefix = "address/{address}/balances_v2/"

        self.covalentApiKey = current_app.config['COVALENT_API']

        pass
    
    def setAddress(self, address):
        self.address = address

    def getAddressBalance(self):
        addressUrl = self.covalentAddressBalancePrefix.format(address=self.address)
        response = requests.get(self.covalentApiUrl.format(prefix=addressUrl), auth=HTTPBasicAuth(self.covalentApiKey, ""))
        if response.status_code >= 500:
            return {"error_message": "Covalenthq api call fail"}, response.statusCode
        return json.loads(response.text), response.status_code

    def getAddressTransactions(self):
        addressUrl = self.covalentAddressTransactionsPrefix.format(address=self.address)
        response = requests.get(self.covalentApiUrl.format(prefix=addressUrl), auth=HTTPBasicAuth(self.covalentApiKey, ""))
        if response.status_code >= 500:
            return {"error_message": "Covalenthq api call fail"}, response.status_code
        return json.loads(response.text), response.status_code

    async def getTransactionLogs(self, transactionIDs):
        Fetch = SessionFetch()
        tasks = []
        async with aiohttp.ClientSession(auth=BasicAuth(self.covalentApiKey, "")) as session:
            for txid in transactionIDs:
                transactionPrefix = self.covalentOneTransactionPrefix.format(transactionID=txid)
                url = self.covalentApiUrl.format(prefix=transactionPrefix)
                response = Fetch.fetch(session, url)
                tasks.append(response)
            fetched = await asyncio.gather(*tasks)

        toJson = []
        for tx in fetched:
            try:
                toJson.append(json.loads(tx))
            except:
                continue
        return toJson