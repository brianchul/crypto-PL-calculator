import { FC, useEffect } from "react";
import { IPair } from "../models/pair";
import { Select } from 'antd';
import { useRef } from "react";

interface ISelectionOption{
    selectedtokens: string[],
    jsondata: IPair 

}

interface IOption{
    key: string,
    value: string,
    description: string
}

const SelectionOptions:FC<ISelectionOption> = (props) => {
    const { Option } = Select;
    const filteredOptions = useRef<IOption[]>([])

    
    useEffect(() => {
        console.log(props.jsondata.current)
    }, [props.jsondata]);

    useEffect(() => {
        let flat = Array.prototype.concat(...props.selectedtokens.map((token:string) => props.jsondata[token] !== undefined ? props.jsondata[token].pairSymbol : []))
        let flag:{[key: string]:number} = {}
        flat.forEach((symbol:string) => {
            if(flag[symbol] === undefined)
                flag[symbol] = 1
            else
            flag[symbol] += 1
        })
        let intersection = Object.keys(flag).filter(key => flag[key] === props.selectedtokens.length)
        filteredOptions.current = intersection.map((symbol:string) => {
            const findOne = props.jsondata[symbol]
            return {
                key: symbol,
                value: findOne.tokenAddress,
                description: findOne.name
            }
        })

    }, [props.jsondata, props.selectedtokens]);

    return (
        <>
        {filteredOptions.current.map(option => {
            return <Option key={option.key} value={option.value}>{option.description}</Option>
        })}
        </>
    )
}

export default SelectionOptions