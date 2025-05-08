export interface RequestResponseData {
    id: number,
    requester_first_name: string,
    requester_last_name: string,
    requester_email: string,
    requester_city: string
    requester_state: string,
    requester_zip: string,
    requester_address: string,
    description: string,
    status: string
}

export interface RequestData {
    data: RequestResponseData
}