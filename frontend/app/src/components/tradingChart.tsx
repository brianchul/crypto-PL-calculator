import { FC, useEffect, useRef, useState } from 'react'
import {createChart, IChartApi, ISeriesApi, UTCTimestamp} from 'lightweight-charts'
import useFetchOne from './fetchApi'
import { IApi } from '../models/api'
import { IChart, IRequestChart } from '../models/chart'
import { DexTrade, ITrade } from '../models/trade'
import {Alert, Button, DatePicker, Divider, Input, Row, Space} from 'antd'


const TradingChart:FC = () => {
    const [fromToken, setFromToken] = useState("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c");
    const [fromTokenName, setFromTokenName] = useState("WBNB");
    const [toToken, setToToken] = useState("0xe9e7cea3dedca5984780bafc599bd69add087d56");
    const [toTokenName, setToTokenName] = useState("BUSD");
    const [mediumToken, setMediumToken] = useState("");
    const [mediumTokenName, setMediumTokenName] = useState("");
    const [interval, setInterval] = useState(60);
    const [since, setSince] = useState(new Date((new Date()).valueOf() - 1000*60*60*24).toISOString());
    const [till, setUntil] = useState(new Date().toISOString());


    const url = "http://localhost:3001/chart/"
    const requestBody = useRef<IRequestChart | null>(null)

    const chart = useRef<IChartApi | null>(null)
    const candlestickSeries= useRef<ISeriesApi<"Candlestick"> | null>(null)
    const {errMsg, responseCode, data,fetchData} = useFetchOne<ITrade>()


    const getSince = (date:any, dateString:string) => {
        setSince(date.toISOString())
    }
    const getUntil = (date:any, dateString:string) => {
        setUntil(date.toISOString())
    }


    const parseChartApi = (api:IApi<ITrade>) => {
        const baseCurrency = api.data.data.ethereum.dexTrades[0].baseCurrency.symbol
        const quoteCurrency = api.data.data.ethereum.dexTrades[0].quoteCurrency.symbol
        const parse:IChart[] = api.data.data.ethereum.dexTrades.map((details:DexTrade) => {
            return{
                time: Math.floor(new Date(details.timeInterval.minute).getTime() / 1000) as UTCTimestamp,
                open: Number(details.open_price),
                high: details.maximum_price,
                low: details.minimum_price,
                close: Number(details.close_price)
            }
        })
        return {parse, baseCurrency, quoteCurrency}
    }

    const makeRequest = async () => {
        await fetchData(url, {
            method: "POST",
            body: JSON.stringify(requestBody.current),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        })

        if(data.current !== undefined && data.current.data !== null){
            return parseChartApi(data.current)
        }
    }
    const calcTokenRatio = (fromToken:IChart[], toToken:IChart[]):IChart[] => {
        let calculated:IChart[] = []
        let baseToken = fromToken
        let quoteToken = toToken
        if(fromToken.length > toToken.length){
            baseToken = toToken
            quoteToken = fromToken
        }

        const startTime = quoteToken[0].time
        const endTime = quoteToken[quoteToken.length-1].time
        calculated = baseToken.filter((value) => {
            return value.time >= startTime && value.time <= endTime
        })
        calculated = calculated.map((value, index) => {
            value.open = value.open / quoteToken[index].open
            value.close = value.close / quoteToken[index].close
            value.high = value.high / quoteToken[index].high
            value.low = value.low / quoteToken[index].low
            return value
        })

        return calculated
    }


    const refreshChart = async () => {
        let setData:IChart[] = []
        if(mediumToken !== ""){
            requestBody.current = {
                fromToken: fromToken,
                toToken: mediumToken,
                interval: interval,
                since: since,
                till: till
            }
            const fromTokenPrice = await makeRequest()

            requestBody.current = {
                fromToken: toToken,
                toToken: mediumToken,
                interval: interval,
                since: since,
                till: till
            }

            const toTokenPrice = await makeRequest()

            if(fromTokenPrice !== undefined && toTokenPrice !== undefined){
                setData = calcTokenRatio(fromTokenPrice.parse, toTokenPrice.parse)
                setFromTokenName(fromTokenPrice.baseCurrency)
                setToTokenName(toTokenPrice.baseCurrency)
                setMediumTokenName(fromTokenPrice.quoteCurrency)
            }


        }else{
            requestBody.current = {
                fromToken: fromToken,
                toToken: toToken,
                interval: interval,
                since: since,
                till: till
            }
            const tokenPrice = await makeRequest()

            if(tokenPrice !== undefined){
                setData = tokenPrice.parse
                setFromTokenName(tokenPrice.baseCurrency)
                setToTokenName(tokenPrice.quoteCurrency)
                setMediumTokenName("")
            }
        }

        if(candlestickSeries.current !== null){
            candlestickSeries.current.setData(setData)
            candlestickSeries.current.priceScale().applyOptions({autoScale:true})
            candlestickSeries.current.applyOptions({title:`${fromTokenName} / ${toTokenName}`}) 
        }

    }
    useEffect(() => {
        chart.current = createChart("tradingchart", {width: 700, height: 600})
        candlestickSeries.current = chart.current.addCandlestickSeries()
        candlestickSeries.current.applyOptions({priceFormat:{precision:10, minMove:0.0000000001}})

        refreshChart()
    }, []);

    return (
        <>
        <Row>
            <Space direction="horizontal" size={12}>
                <span>from:</span>
                <Input placeholder="from token" onChange={(e) => {setFromToken(e.target.value)}} />
                <span>to:</span>
                <Input placeholder="to token" onChange={(e) => {setToToken(e.target.value)}} />
                <span>medium:</span>
                <Input placeholder="medium token" onChange={(e) => {setMediumToken(e.target.value)}} />
                <span>interval:</span>
                <Input placeholder="interval" onChange={(e) => {setInterval(Number(e.target.value))}} />
            </Space>

        </Row>
        <Space direction="horizontal" size={12}>
            <span>Since:</span>
            <DatePicker onChange={getSince} showTime={true}/>
            <span>Until:</span>
            <DatePicker onChange={getUntil} showTime={true}/>
            <Divider />
        </Space>
        <Button onClick={refreshChart} >refresh</Button>

        <Divider />
        {mediumTokenName !== "" ? <div>Pair: {fromTokenName} to {toTokenName}; base: {mediumTokenName} </div> :<div>Pair: {fromTokenName} to {toTokenName}</div>}
        <div id="tradingchart"> </div>
        {responseCode > 200 && <Alert message={errMsg} type="error" banner />}
        </>
    )
}

export default TradingChart


