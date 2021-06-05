import requests
from requests.models import HTTPBasicAuth

class Convalenthq():
    def __init__(self) -> None:
        self.address = ""
        self.transaction = ""
        pass

    def queryConvalenthq(url):
        response = requests.get(url, auth=HTTPBasicAuth("ckey_75ec2368885f44c6abb4f325006", ""))
        return response.text, response.status_code

    def addAddress(self, address):
        self.address = address

    def addTransaction(self, transaction):
        self.transaction = transaction

    def findTransaction():
        
        pass

    def findAccountBalances():
        pass

    def find():
        pass