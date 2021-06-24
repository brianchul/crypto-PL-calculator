import {useState, useRef} from 'react'
import {IApi} from '../models/api';
const useFetchOne = <T,>() => {
    const [status, setStatus] = useState("idle");
    const [responseCode, setResponseCode] = useState(0);
    const [errMsg, setErrMsg] = useState("None");
    const data = useRef<IApi<T>>()

    const fetchData = async (url:string, options?:RequestInit) =>{
        if(url !== "") {
            setStatus('fetching...')
            const response = await fetch(url, options)
            const json:IApi<T> = await response.json()
            const code = response.status
            setResponseCode(code)
            data.current = json
            setStatus("fetched")
            setErrMsg(json.description === null ? "None" : json.description)
        }
    }

    const clearUrl = () => {

        setStatus("idle")

    }

    return {status, errMsg, data, clearUrl, responseCode, fetchData}
}
export default useFetchOne