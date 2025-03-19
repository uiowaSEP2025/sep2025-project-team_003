export interface InvoiceQuoteDisplayInterface {
    'quotes': QuoteJSON[],
    'totalMaterialSubtotal': string
    'totalPrice': string
}

export interface QuoteJSON{
    "materialSubtotal": string,
    "totalPrice": string,
    "jobDescription": string
  }