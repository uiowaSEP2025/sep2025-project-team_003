export interface RequestResponseData {
    id: number,
    requestor_name: string,
    requestor_email: string,
    requestor_city: string
    requestor_state: string,
    requestor_zip: string,
    requestor_address: string,
    description: string,
    status: string
}

export interface RequestData {
    data: RequestResponseData
}