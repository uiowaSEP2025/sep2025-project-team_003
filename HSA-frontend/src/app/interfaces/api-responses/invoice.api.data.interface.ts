import { InvoiceQuoteDisplayInterface } from "../invoice.quote.display.interface"
export interface InvoiceDataInterface {
    id: number, 
    status: 'created' | 'issued' | 'paid',
    issuanceDate: string
    dueDate: string ,
    customer: string,
    quotes: InvoiceQuoteDisplayInterface[]
}