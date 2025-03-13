interface Quote {
    materialSubtotal: number,
    totalPrice: number,
    truncatedJobDescription: string
}

export interface InvoiceDataInterface {
    id: number, 
    status: 'created' | 'issued' | 'paid',
    dueDate: string ,
    customer: string,
    quotes: Quote[]
}