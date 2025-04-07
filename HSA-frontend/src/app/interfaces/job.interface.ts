import {Customer} from './customer.interface';
import {Service} from './service.interface';
import {Material} from './material.interface';

export interface Job {
 id: number
 jobStatus: 'created' | 'in-progress' | 'completed'
 startDate: Date
 endDate: Date
 description: string
 customer: Customer
 services: Service[]
 materials: Material[]
 jobAddress: string
 jobCity: string
 jobState: string
 jobZip: string
}
