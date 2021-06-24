import asyncio
import aiohttp
from aiohttp.helpers import BasicAuth
import requests
from requests.models import HTTPBasicAuth
import json
from flask import current_app


from ..extension.requestFetch import SessionFetch


class Convalenthq():
    MAX_RETRY = 10
    def __init__(self) -> None:
        self.address = ""
        self.transaction = ""
        self.covalentApiUrl = "https://api.covalenthq.com/v1/56/{prefix}"
        self.covalentOneTransactionPrefix = "transaction_v2/{transactionID}/"
        self.covalentAddressTransactionsPrefix = "address/{address}/transactions_v2/?page-size=9999&block-signed-at-asc=false"

        self.covalentApiKey = current_app.config['COVALENT_API']

        pass

    def getAddressTransactions(self, address):
        addressUrl = self.covalentAddressTransactionsPrefix.format(address=address)
        response = requests.get(self.covalentApiUrl.format(prefix=addressUrl), auth=HTTPBasicAuth(self.covalentApiKey, ""))
        return json.loads(response.text), response.status_code

    async def getTransactionLogs(self, transactionIDs):
        Fetch = SessionFetch()
        tasks = []
        async with aiohttp.ClientSession(auth=BasicAuth(self.covalentApiKey, "")) as session:
            for txid in transactionIDs:
                
                transactionPrefix = self.covalentOneTransactionPrefix.format(transactionID=txid)
                url = self.covalentApiUrl.format(prefix=transactionPrefix)
                tasks.append(Fetch.fetch(session, url))
            fetched = await asyncio.gather(*tasks)
        return fetched