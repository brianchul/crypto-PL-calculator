import requests
from requests.models import HTTPBasicAuth
import json
import configparser



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

    def getTransactionLogs(self, transactionID):
        transactionPrefix = self.covalentOneTransactionPrefix.format(transactionID=transactionID)
        url = self.covalentApiUrl.format(prefix=transactionPrefix)

        response = requests.get(url, auth=HTTPBasicAuth(self.covalentApiKey, ""))
        return json.loads(response.text), response.status_code