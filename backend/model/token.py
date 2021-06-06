from backend.model.transaction import Transaction


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
