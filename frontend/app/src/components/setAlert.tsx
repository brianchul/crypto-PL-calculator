import { Alert } from "antd";
import { FC } from "react";


interface IAlert{
    type: 'success' | 'info' | 'warning' | 'error'
    message: string
}
export const SetAlert:FC<IAlert> = (props) => {
    return(
        <Alert message={props.message} type={props.type} banner />
    )
}