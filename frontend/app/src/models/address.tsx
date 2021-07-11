export interface IAddressData {
    name: string
    info: IAddressInfo
    transaction: [{
        costUsd: number
        createTime: string
        fromToken: string
        toToken: string
        fromTokenAmount: number
        toTokenAmount: number
        transactionHash: string
    }]
}

export interface IAddressInfo{
    name: string
    amount: number
    costAvg: number
    usdValue: number
}