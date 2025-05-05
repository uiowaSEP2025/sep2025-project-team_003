import { InvoiceQuoteDisplayInterface } from "./invoice.quote.display.interface"
export interface InvoiceDataInterface {
    id: number,
    status: 'created' | 'issued' | 'paid',
    dateIssued: string
    dateDue: string ,
    customer: {
      first_name: string,
      last_name: string,
      notes: string,
      email: string,
      phone: string,
      id: number
    },
    quotes: InvoiceQuoteDisplayInterface
}
