
export interface JobGeneralDataInterface {
    id: number, 
    jobStatus: 'created' | 'completed',
    startDate: string
    endDate: string ,
    description: string,
    customerName: string,
    customerID: number,
    requestorAddress: string,
    requestorCity: string,
    requestorState: string,
    requestorZip: string,
}