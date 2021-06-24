export interface IApi<T> {
    data: T,
    code: number,
    description: string | null
    msg: string | null
    timestamp: number
}