import {Customer} from './customer.interface';
import {Service} from './service.interface';
import {Material} from './material.interface';

export interface JobSimple {
  id: number
  jobStatus: 'created' | 'in-progress' | 'completed'
  startDate: Date
  endDate: Date
  description: string
}

export interface JobTable extends JobSimple {
  customerName: string
}

export interface Job extends JobSimple {
 customer: Customer
 services: Service[]
 materials: Material[]
 jobAddress: string
 jobCity: string
 jobState: string
 jobZip: string
}
