import { FC, useEffect, useRef, useState } from "react";
import { Button, DatePicker, Divider, Input, Select, Space, Spin } from 'antd';
import useFetchOne from './fetchApi'
import { IPair } from "../models/pair";

interface IAddressSelector {
    selected: (fromToken?: string, toToken?: string, mediumToken?: string, interval?: number, since?: string, till?: string) => void
}

interface IOption {
    key: string,
    value: string,
    description: string
}

export const AddressSelector: FC<IAddressSelector> = (props) => {
    const optionData = useRef<{ [tokenName: string]: IOption }>({})
    const { data, fetchData } = useFetchOne<IPair>()

    const [fromToken, setFromToken] = useState("");
    const [fromTokenName, setFromTokenName] = useState("");
    const [toToken, setToToken] = useState("");
    const [toTokenName, setToTokenName] = useState("");
    const [mediumToken, setMediumToken] = useState("");
    const [mediumTokenName, setMediumTokenName] = useState("");
    const [interval, setInterval] = useState(60);
    const [since, setSince] = useState(new Date((new Date()).valueOf() - 1000 * 60 * 60 * 24).toISOString());
    const [till, setUntil] = useState(new Date().toISOString());

    const onChangeFromToken = (value: string, option: any) => {
        if (option === undefined || value === "") {
            setFromToken("")
            setFromTokenName("")
        } else {
            setFromToken(value)
            setFromTokenName(option.children)
        }
    }
    const onChangeToToken = (value: string, option: any) => {
        if (option === undefined || value === "") {
            setToToken("")
            setToTokenName("")
        } else {
            setToToken(value)
            setToTokenName(option.children)
        }
    }
    const onChangeMediumToken = (value: string, option: any) => {
        if (option === undefined || value === "") {
            setMediumToken("")
            setMediumTokenName("")
        } else {
            setMediumToken(value)
            setMediumTokenName(option.children)
        }
    }

    const getSince = (date: any, dateString: string) => {
        setSince(date.toISOString())
    }
    const getUntil = (date: any, dateString: string) => {
        setUntil(date.toISOString())
    }
    const cakeBunny = () => {
        setFromToken("0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82")
        setMediumToken("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")
        setToToken("0xc9849e6fdb743d08faee3e34dd2d1bc69ea11a51")
        setFromTokenName("Cake")
        setMediumTokenName("WBNB")
        setToTokenName("Bunny")
    }
    const cakeBp = () => {
        setFromToken("0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82")
        setMediumToken("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")
        setToToken("0xacb8f52dc63bb752a51186d1c55868adbffee9c1")
        setFromTokenName("Cake")
        setMediumTokenName("WBNB")
        setToTokenName("BP")
    }
    const cakeBusd = () => {
        setFromToken("0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82")
        setMediumToken("")
        setToToken("0xe9e7cea3dedca5984780bafc599bd69add087d56")
        setFromTokenName("Cake")
        setMediumTokenName("")
        setToTokenName("BUSD")
    }

    const fetchOptions = async () => {
        await fetchData("/chart/chartPair")
    }

    useEffect(() => {
        if (data.current !== undefined && data.current !== null && data.current.data !== null)
            Object.keys(data.current.data).map(token => {
                if (data.current !== undefined)
                    optionData.current[token] = {
                        key: token,
                        value: data.current.data[token].tokenAddress,
                        description: data.current.data[token].name

                    }
            })
        else
            fetchOptions()
    }, [data.current]);

    useEffect(() => {
        props.selected(fromToken, toToken, mediumToken, interval, since, till)
    }, [fromToken, toToken, mediumToken, interval, since, till]);


    return (
        <>
            <Space direction="horizontal" size={12}>
                <span>from:</span>
                <Input placeholder="token address" onChange={(e) => { setFromToken(e.target.value) }} allowClear={true} value={fromToken} />
                <span>to:</span>
                <Input placeholder="token address" onChange={(e) => { setToToken(e.target.value) }} allowClear={true} value={toToken} />
            </Space>
            <Space direction="horizontal" size={12}>
                <span>medium:</span>
                <Input placeholder="optional" onChange={(e) => { setMediumToken(e.target.value) }} allowClear={true} value={mediumToken} />
                <span>minute interval:</span>
                <Input placeholder="60" onChange={(e) => { setInterval(Number(e.target.value)) }} allowClear={true} />
            </Space>
            <Space direction="horizontal" size={12}>
            <Select
                showSearch
                style={{ width: 200 }}
                placeholder="Select base token"
                onChange={onChangeFromToken}
                filterOption={(input, option) =>
                    option?.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                }
                allowClear={true}
            >
                {optionData.current !== null ? Object.keys(optionData.current).map(token => {
                    if (![mediumTokenName, toTokenName].includes(token))
                        return <Select.Option key={optionData.current[token].description} value={optionData.current[token].value}>{token}</Select.Option>
                    else return <Select.Option key={optionData.current[token].description} value={optionData.current[token].value} disabled={true}>{token}</Select.Option>
                }) : <Spin size="small" />}
            </Select>

            <Select
                showSearch
                style={{ width: 200 }}
                placeholder="Select medium token"
                onChange={onChangeMediumToken}
                filterOption={(input, option) =>
                    option?.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                }
                allowClear={true}
            >
                {optionData.current !== null ? Object.keys(optionData.current).map(token => {
                    if (![fromTokenName, toTokenName].includes(token))
                        if (fromTokenName !== "" && !data.current?.data[fromTokenName]?.pairSymbol.includes(token)) { }
                        else if (toTokenName !== "" && !data.current?.data[toTokenName]?.pairSymbol.includes(token)) { }
                        else return <Select.Option key={optionData.current[token].description} value={optionData.current[token].value}>{token}</Select.Option>
                }) : <Spin size="small" />}
            </Select>

            <Select
                showSearch
                style={{ width: 200 }}
                placeholder="Select to token"
                onChange={onChangeToToken}
                filterOption={(input, option) =>
                    option?.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                }
                allowClear={true}
            >
                {optionData.current !== null ? Object.keys(optionData.current).map(token => {
                    if (![fromTokenName, mediumTokenName].includes(token))
                        return <Select.Option key={optionData.current[token].description} value={optionData.current[token].value}>{token}</Select.Option>
                    else return <Select.Option key={optionData.current[token].description} value={optionData.current[token].value} disabled={true}>{token}</Select.Option>
                }) : <Spin size="small" />}
            </Select>
            </Space>
            <Divider/>
            <Space direction="horizontal" size={12}>
                <span>Since:</span>
                <DatePicker onChange={getSince} showTime={true} />
                <span>Until:</span>
                <DatePicker onChange={getUntil} showTime={true} />
                <Divider />
            </Space>
            <Divider />
            <Space direction="horizontal" size={12}>
                <Button onClick={cakeBunny} >CAKE TO BUNNY</Button>
                <Button onClick={cakeBp} >CAKE TO BP</Button>
                <Button onClick={cakeBusd} >CAKE TO BUSD</Button>
            </Space>
            {mediumTokenName !== "" ? <div>Pair: {fromTokenName} to {toTokenName}; base: {mediumTokenName} </div> : <div>Pair: {fromTokenName} to {toTokenName}</div>}

        </>

    )
}