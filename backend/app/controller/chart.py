from datetime import datetime, timedelta, timezone
from flask import abort, current_app
import requests, json




def queryPrice(fromToken="0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c", toToken="0xe9e7cea3dedca5984780bafc599bd69add087d56", interval=60, since=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat(),till=datetime.now(timezone.utc).isoformat()):
    bigQueryAPIKEY = current_app.config["BIGQUERY_API"]
    header = {
        "X-API-KEY": bigQueryAPIKEY
    }
    body = {
        "query": "query GetCandleData(\n  $baseCurrency: String!,\n  $since: ISO8601DateTime,\n  $till: ISO8601DateTime,\n  $quoteCurrency: String!,\n  $exchangeAddresses: [String!]\n  $minTrade: Float\n  $window: Int) {\n    ethereum(network: bsc) {\n        dexTrades(\n            options: {asc: \"timeInterval.minute\"}\n            date: {since: $since, till: $till}\n            exchangeAddress: {in: $exchangeAddresses}\n            baseCurrency: {is: $baseCurrency}\n            quoteCurrency: {is: $quoteCurrency} # WBNB\n            tradeAmountUsd: {gt: $minTrade}\n        ) {\n            timeInterval {\n                minute(count: $window, format: \"%Y-%m-%dT%H:%M:%SZ\")\n            }\n            baseCurrency {\n                symbol\n                address\n            }\n            quoteCurrency {\n                symbol\n                address\n            }\n\n            tradeAmount(in: USD)\n            trades: count\n            quotePrice\n            maximum_price: quotePrice(calculate: maximum)\n            minimum_price: quotePrice(calculate: minimum)\n            open_price: minimum(of: block, get: quote_price)\n            close_price: maximum(of: block, get: quote_price)\n        }\n    }\n}\n",
        "variables": {
            "baseCurrency": fromToken,
            "quoteCurrency": toToken,
            "since": since,
            "till": till,
            "window": int(interval),
            "minTrade": 10
        }
    }
    url = "https://graphql.bitquery.io"
    try:
        resp = requests.post(url=url,headers=header, json=body)
        if resp.status_code != 200:
            abort(resp.status_codes,resp.text)
        elif "errors" in json.loads(resp.text):
            abort(400, json.loads(resp.text)["errors"][0]["message"])
        return resp.text
    except Exception as e:
        current_app.logger.warn(json.dumps(body["variables"]))
        current_app.logger.error(e)
        abort(500, "There's an error")