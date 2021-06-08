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