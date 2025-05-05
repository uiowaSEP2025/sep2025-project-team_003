export interface JobTemplateDisplayInterface {
    'services': ServiceJSON[],
    'materials': MaterialJSON[],
    'contractors': ContractorJSON[]
}

export interface ServiceJSON{
    "id": string,
    "name": string,
    "description": string
    "fee": number,
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
