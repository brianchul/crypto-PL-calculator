import { FC, useRef } from 'react'
import {IApi} from '../models/api'
import {IAddressData, IAddressInfo} from '../models/address'
import { Table as AntTable } from 'antd'

interface ITable{
    api: IApi<IAddressData[]> | undefined
}

interface IColumns{
    title: string
    dataIndex: string
    key: string
}

interface IDataSources extends IAddressInfo{
    key: string
}


const Table:FC<ITable> = (props) => {

    const columns = useRef<IColumns[]>([]);
    const dataSource = useRef<IDataSources[]>([]);


    if (props.api !== undefined){
        columns.current = ["name", "amount", "usdValue", "costAvg"].map((key, index) => {
            return { title: key , dataIndex: key, key: key}
        })

        dataSource.current = props.api.data.map((row, index) => {
            return {key: index.toString(), name: row.info.name, amount:row.info.amount, costAvg: row.info.costAvg, usdValue: row.info.usdValue}
        })

    }

    return  props.api === undefined || props.api.data === null  ? <div>No data</div> :
        <AntTable dataSource={dataSource.current} columns={columns.current} />;
    
}

export default Table