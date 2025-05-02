import { InvoiceQuoteDisplayInterface } from "./invoice.quote.display.interface"
export interface InvoiceDataInterface {
    id: number,
    status: 'created' | 'issued' | 'paid',
    dateIssued: string
    dateDue: string ,
    customer: {
      email: string,
      first_name: string,
      id: number,
      last_name: string,
      notes: string,
      phone: string,
    },
    quotes: InvoiceQuoteDisplayInterface
    jobs: number[]
}
