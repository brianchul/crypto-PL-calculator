import { useState, FC } from 'react'
import useFetchOne from './fetchApi'
import Table from './tables'
import TradingChart from './tradingChart'
import { IAddressData } from '../models/address'
import { Button, Col, Input, Row } from 'antd'

const MainPage:FC=()=>{
    const [account, setAccount] = useState("");
    const [url, setFullUrl] = useState("/account/");
    const baseUrl = "/account/"
    const { status, errMsg, data, clearUrl, fetchData } = useFetchOne<IAddressData[]>()
    const [showBackendBtn, setShowBackendBtn] = useState(false);
    const [changeShowBackendBtn, setChangeShowBackendBtn] = useState("show backend api data");

    const FetchAccount = async () => {
        await fetchData(url)
    }
    const GetAccount = (acc:string) => {
        setAccount(acc)
        setFullUrl(baseUrl + acc)
    }

    const ShowBackend = () => {
        setShowBackendBtn(!showBackendBtn)
        if(!showBackendBtn)
            setChangeShowBackendBtn("hide backend api data")
        else
            setChangeShowBackendBtn("show backend api data")
    }

   
    return (
        <Row>
            <Col span={10}  offset={1}>
                <Input placeholder="Address" onChange={(e) => {GetAccount(e.target.value)}} />
                <Button onClick={FetchAccount}>
                    get account
                </Button>

                <Button onClick={clearUrl}>clear content</Button>
                <Button onClick={ShowBackend}>{changeShowBackendBtn}</Button>
                
                <div>status: {status}</div>
                <div>Error message: {errMsg}</div>
                <div id="showApi">{showBackendBtn ? JSON.stringify(data) : ""}</div>
                <Table api={data.current} />
            </Col>
            <Col span={10} offset={1}>
                <TradingChart/>

            </Col>
        </Row>
    )
}


export default MainPage