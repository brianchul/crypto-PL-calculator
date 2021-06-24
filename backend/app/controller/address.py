from flask import abort
import asyncio
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
    covalentApi = Convalenthq()
    covalentApi.setAddress(address)
    newPriceApi = Price()

    r, code = covalentApi.getAddressBalance()
    if code != 200:
        abort(code, description=r["error_message"])
        #return json.dumps(r)

    r, code = covalentApi.getAddressTransactions()
    data = r
    history = TokenHistory()
    totalTransactions = 0
    matchedTransactions = []
    for j in data["data"]["items"]:
        if len(j["log_events"]) == 0 or j["log_events"][0]["decoded"] == None or j["log_events"][0]["decoded"]["name"] != "Swap":
            continue

        totalTransactions += 1
        matchedTransactions.append(j["tx_hash"])

    if len(matchedTransactions) == 0:
        return []


    loop = asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()
    fetchTransactions = loop.run_until_complete(covalentApi.getTransactionLogs(matchedTransactions))

    if len(fetchTransactions) == 0:
        abort(500, "unable to fetch transaction detail")
    for transactionDetail in fetchTransactions:

        fromToken = ""
        fromTokenAmount = 0
        toToken = ""
        toTokenAmount = 0
        swapCostUsd = 0
        swapDate = datetime.fromisoformat(datetimeIsoFormatCleanup(transactionDetail["data"]["items"][0]["block_signed_at"]))

        for i in transactionDetail["data"]["items"][0]["log_events"]:
            if "decoded" in i and "name" in i["decoded"] and i["decoded"]["name"] == "Transfer":
                symbol = i["sender_contract_ticker_symbol"]
                tokenValue = int(i["decoded"]["params"][2]["value"])
                tokenDecimal = 10 ** int(i["sender_contract_decimals"])
                tokenValue = tokenValue / tokenDecimal

                if "BNB" in symbol and swapCostUsd == 0:
                    bnbPrice = loop.run_until_complete(newPriceApi.getBNBprice(swapDate))

                    swapCostUsd = bnbPrice*tokenValue
                elif "USD" in symbol:
                    swapCostUsd = tokenValue

                if toToken == "":
                    toToken = symbol
                    toTokenAmount = tokenValue
                fromToken = symbol
                fromTokenAmount = tokenValue

        newTransaction = Transaction(transactionDetail["data"]["items"][0]["tx_hash"], fromToken, fromTokenAmount, toToken, toTokenAmount, swapCostUsd, swapDate.isoformat())
        history.addTransaction(newTransaction)
    return history.printAll()

