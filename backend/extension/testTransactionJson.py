import json
f = open("addressTransactionHistory.json")
data = json.load(f)

for j in data["data"]["items"]:
    
    if len(j["log_events"]) == 0 or j["log_events"][0]["decoded"] == None or j["log_events"][0]["decoded"]["name"] != "Swap":
        continue
    print(j["tx_hash"])
    
    for i in j["log_events"]:
        if i["decoded"]["name"] == "Transfer":
            tokenName = i["sender_name"]
            symbol = i["sender_contract_ticker_symbol"]
            tokenValue = int(i["decoded"]["params"][2]["value"])
            tokenDecimal = 10 ** int(i["sender_contract_decimals"] if i["sender_contract_decimals"] != None else 18)
            tokenValue = tokenValue / tokenDecimal
            print(tokenName, symbol, tokenValue)
    print()

f.close() 