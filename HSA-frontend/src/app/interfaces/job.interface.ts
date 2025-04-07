export interface Job {
 id: number
 jobStatus: 'created' | 'in-progress' | 'completed'
 startDate: Date
 endDate: Date
 description: string
 customerName: string
 customerID: number
 requesterAddress: string
 requesterCity: string
 requesterState: string
 requesterZip: string
}
