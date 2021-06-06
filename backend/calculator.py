import requests
from requests.models import HTTPBasicAuth
import json
from datetime import datetime, timedelta
import configparser

config =configparser.ConfigParser()
config.read("config.ini")
covalentApiKey = config["DEFAULT"]["covalentApiKey"]
bscAddress = config["DEFAULT"]["bscAddress"]

covalentApiUrl = "https://api.covalenthq.com/v1/56/{prefix}"
covalentOneTransactionPrefix = "transaction_v2/{transactionID}/"
covalentAddressTransactionsPrefix = "address/{address}/transactions_v2/?page-size=9999&block-signed-at-asc=false"
binanceApiUrl = "https://api.binance.com/api/v3/klines"

def getAddressTransactions(address):
    addressUrl = covalentAddressTransactionsPrefix.format(address=address)
    response = requests.get(covalentApiUrl.format(prefix=addressUrl), auth=HTTPBasicAuth(covalentApiKey, ""))
    return json.loads(response.text), response.status_code

def getTransactionLogs(transactionID):
    transactionPrefix = covalentOneTransactionPrefix.format(transactionID=transactionID)
    url = covalentApiUrl.format(prefix=transactionPrefix)

    response = requests.get(url, auth=HTTPBasicAuth(covalentApiKey, ""))
    return json.loads(response.text), response.status_code

def getBNBprice(startTime: datetime):
    endTime = startTime + timedelta(minutes=1)
    parameters = {
        "symbol": "BNBUSDT",
        "interval": "1m",
        "startTime": bnbApiTimestampFormat(startTime),
        "endTime": bnbApiTimestampFormat(endTime)
    }
    response = requests.get(binanceApiUrl, params=parameters)
    if response.text == "":
        return 0
    price = float(json.loads(response.text)[0][1])
    return price

def datetimeIsoFormatCleanup(isoFormat):
    return isoFormat[:-1]+".000000"+"+00:00"

def bnbApiTimestampFormat(dt: datetime):
    timestamp = dt.timestamp()
    timestamp = timestamp * 1000
    return int(timestamp)


class Token(object):
    def __init__(self, name: str) -> None:
        self.name = name
        self.amount = 0
        self.usdValue = 0
        self.costAvg = 0
        pass
    def addAmount(self, amount, usdValue):
        self.amount += amount
        self.usdValue += usdValue
        return
    def subAmount(self, amount, usdValue):
        self.amount -= amount
        self.usdValue -= usdValue
        return
    def updateCostAvg(self):
        if self.amount > 0:
            self.costAvg = self.usdValue / self.amount
        return

class Transaction(object):
    def __init__(self, transactionHash:str, fromToken: str, fromTokenAmount: float, toToken: str, toTokenAmount: float, costUsd: float, createTime: str) -> None:
        self.transactionHash = transactionHash
        self.fromToken = fromToken
        self.fromTokenAmount = fromTokenAmount
        self.toToken = toToken
        self.toTokenAmount = toTokenAmount
        self.costUsd = costUsd
        self.createTime = createTime
        pass


class TokenHistory():
    def __init__(self) -> None:
        self.history = {}
        pass

    def findToken(self, tokenName):
        if self.history[tokenName] != None:
            return self.history[tokenName]
        return None

    def newToken(self, tokenName: str):
        self.history[tokenName] = {"info": Token(tokenName), "transaction":[]}

    def addTransaction(self, transaction: Transaction):
        fromToken = transaction.fromToken
        toToken = transaction.toToken

        if fromToken not in self.history:
            self.newToken(fromToken)

        self.history[fromToken]["info"].subAmount(transaction.fromTokenAmount, transaction.costUsd)
        self.history[fromToken]["transaction"].append(transaction)
        self.history[fromToken]["info"].updateCostAvg()

        if toToken not in self.history:
            self.newToken(toToken)

        self.history[toToken]["info"].addAmount(transaction.toTokenAmount, transaction.costUsd)
        self.history[toToken]["transaction"].append(transaction)
        self.history[toToken]["info"].updateCostAvg()
        return

    def printOne(self, tokenName):
        output = {}
        if tokenName in self.history:

            info = self.history[tokenName]["info"]
            transactions = self.history[tokenName]["transaction"]
            output["info"] = info.__dict__
            output["transaction"] = [t.__dict__ for t in transactions]

        return output

    def printAll(self):
        output = []
        for key in self.history:
            info = self.history[key]["info"]
            transactions = self.history[key]["transaction"]

            token = {}
            token["name"] = key
            token["info"] = info.__dict__
            token["transaction"] = [t.__dict__ for t in transactions]
            output.append(token)

        return output



r, code = getAddressTransactions(bscAddress)
if code != 200:
    print(json.dumps(r))
data = r
history = TokenHistory()
totalTransactions = 0
for j in data["data"]["items"]:
    if len(j["log_events"]) == 0 or j["log_events"][0]["decoded"] == None or j["log_events"][0]["decoded"]["name"] != "Swap":
        continue
    print(j["tx_hash"])
    totalTransactions += 1
    transactionDetail, code = getTransactionLogs(j["tx_hash"])

    fromToken = ""
    fromTokenAmount = 0
    toToken = ""
    toTokenAmount = 0
    swapCostUsd = 0
    swapDate = datetime.fromisoformat(datetimeIsoFormatCleanup(j["block_signed_at"]))

    for i in transactionDetail["data"]["items"][0]["log_events"]:
        if i["decoded"]["name"] == "Transfer":
            tokenName = i["sender_name"]
            symbol = i["sender_contract_ticker_symbol"]
            tokenValue = int(i["decoded"]["params"][2]["value"])
            tokenDecimal = 10 ** int(i["sender_contract_decimals"])
            tokenValue = tokenValue / tokenDecimal

            if "BNB" in symbol and swapCostUsd == 0:
                bnbPrice = getBNBprice(swapDate)
                swapCostUsd = bnbPrice*tokenValue
            elif "USD" in symbol:
                swapCostUsd = tokenValue

            if toToken == "":
                toToken = symbol
                toTokenAmount = tokenValue
            fromToken = symbol
            fromTokenAmount = tokenValue

    newTransaction = Transaction(j["tx_hash"], fromToken, fromTokenAmount, toToken, toTokenAmount, swapCostUsd, swapDate.isoformat())
    history.addTransaction(newTransaction)
    


fp = open("transactions.json", "w")
fp.write(json.dumps(history.printAll()))
fp.close()
print("Total transactions: {a}".format(a=totalTransactions))