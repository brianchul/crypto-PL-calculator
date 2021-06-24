import { FC } from 'react'
import {IApi} from '../models/api'
import {IAddressData} from '../models/address'
import '../style/table.css'

interface ITable{
    api: IApi<IAddressData[]> | undefined
}



const Table:FC<ITable> = (props) => {


    return  props.api === undefined || props.api.data === null  ? <div>No data</div> :
        <table>
            <thead>
                <tr>{
                        Object.keys(props.api.data[0].info).map((key, index) => {
                            return <th key={key}>{key.toUpperCase()}</th>
                        })
                    }</tr>
            </thead>
            <tbody>{
                props.api.data.map((row, index) => {
                    return <tr key={index}><RenderRow key={index} data={row.info} keys={Object.keys(row.info)}></RenderRow></tr>
                })
            }</tbody>
        </table>
    
}

const RenderRow = (props:any) => {
    return (
        <>
            {props.keys.map((key:string) => {
                return <td key={props.data[key]}>{props.data[key]}</td>
            })}
        </>
    )
    
}

export default Table