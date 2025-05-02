export interface JobDisplayInterface {
    'services': ServiceJSON[],
    'materials': MaterialJSON[],
    'contractors': ContractorJSON[],
}

export interface ServiceJSON{
    "fee": number,
    "id": string,
    "name": string,
    "description": string
}

export interface MaterialJSON{
    "materialID": string,
    "materialName": string,
    "unitsUsed": string,
    "pricePerUnit": string
}

export interface ContractorJSON{
    "contractorID": string,
    "contractorName": string,
    "contractorPhoneNo": string,
    "contractorEmail": string
}
