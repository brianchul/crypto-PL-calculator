import json
from datetime import datetime
from ..extension.covalenthq import Convalenthq
from ..extension.datetimeparser import datetimeIsoFormatCleanup
from ..extension.price import Price
from ..model.token import TokenHistory
from ..model.transaction import Transaction

def getOneTransaction(txid: str):
    pass

def analysisToken(address: str):
    newCovalenthqApi = Convalenthq()
    newPriceApi = Price()

    r, code = newCovalenthqApi.getAddressTransactions(address)
    if code != 200:
        print(json.dumps(r))
        return json.dumps(r)
    data = r
    history = TokenHistory()
    totalTransactions = 0
    for j in data["data"]["items"]:
        if len(j["log_events"]) == 0 or j["log_events"][0]["decoded"] == None or j["log_events"][0]["decoded"]["name"] != "Swap":
            continue
        print(j["tx_hash"])
        totalTransactions += 1
        transactionDetail, code = newCovalenthqApi.getTransactionLogs(j["tx_hash"])

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
                    bnbPrice = newPriceApi.getBNBprice(swapDate)
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
    return json.dumps(history.printAll())

