export interface JobTemplateDisplayInterface {
    'services': ServiceJSON[],
    'materials': MaterialJSON[]
}

export interface ServiceJSON{
    "serviceID": string,
    "serviceName": string,
    "serviceDescription": string
}

export interface MaterialJSON{
    "materialID": string,
    "materialName": string,
    "unitsUsed": string,
    "pricePerUnit": string
}