import {Job} from './job.interface';
import {Discount} from './discount.interface';
import {Customer} from './customer.interface';

export interface Invoice {
  invoiceID: number;
  customer: Customer;
  invoiceIssueDate: Date;
  invoiceDueDate: Date;
  invoiceStatus: "created" | "issued" | "paid"
  invoicePrice: number;
  invoiceTax: number;
  jobs: Job[];
  discounts: Discount[];
}
