import { useState, FC } from 'react'
import useFetchOne from './fetchApi'
import Table from './tables'
import TradingChart from './tradingChart'
import { IAddressData } from '../models/address'
import { Button, Col, Input, Row, Space } from 'antd'

const MainPage: FC = () => {
    const [url, setFullUrl] = useState("/account/");
    const baseUrl = "/account/"
    const { status, errMsg, data, clearUrl, fetchData } = useFetchOne<IAddressData[]>()
    const [showBackendBtn, setShowBackendBtn] = useState(false);
    const [changeShowBackendBtn, setChangeShowBackendBtn] = useState("show backend api data");

    const FetchAccount = async () => {
        await fetchData(url)
    }
    const GetAccount = (acc: string) => {
        if(acc.indexOf("/") === -1)
            acc += "/"
        setFullUrl(baseUrl + acc)
    }

    const ShowBackend = () => {
        setShowBackendBtn(!showBackendBtn)
        if (!showBackendBtn)
            setChangeShowBackendBtn("hide backend api data")
        else
            setChangeShowBackendBtn("show backend api data")
    }


    return (
        <Row>
            <Col offset={1} lg={12} xl={11}>
                <Space direction="vertical">
                    <div>You can type "test" as address to get example analysis</div>
                    <Input placeholder="Address" onChange={(e) => { GetAccount(e.target.value) }} />
                    <Button onClick={FetchAccount}>
                        get account
                    </Button>
                </Space>

                {/* <Button onClick={clearUrl}>clear content</Button>
                <Button onClick={ShowBackend}>{changeShowBackendBtn}</Button> */}
                <div>
                    <Space>
                        <div>status: {status}</div>
                        <div>Error message: {errMsg}</div>
                        <div id="showApi">{showBackendBtn ?
                            <Input.TextArea rows={4} value={JSON.stringify(data)} /> : ""}
                        </div>
                    </Space>
                </div>
                <Table api={data.current} />
            </Col>
            <Col offset={1} lg={12} xl={11}>
                <TradingChart />
            </Col>
        </Row>
    )
}


export default MainPage