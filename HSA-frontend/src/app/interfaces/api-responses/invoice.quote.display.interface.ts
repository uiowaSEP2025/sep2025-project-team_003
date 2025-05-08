export interface InvoiceQuoteDisplayInterface {
    'quotes': QuoteJSON[],
    "totalMaterialSubtotal": string,
    "subtotal": string,
    "taxPercent": string,
    "totalDiscount": string,
    "grandtotal" : string,
}

export interface QuoteJSON{
    "materialSubtotal": string,
    "totalPrice": string,
    "jobDescription": string
  }