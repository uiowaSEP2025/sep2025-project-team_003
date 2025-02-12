export interface Quote {
  quoteID: number;
  jobID: number;
  discountID: number;
  quoteDate: Date;
  quoteStatus: string;
  quoteMaterialSubTotal: number;
  quoteTotalPrice: number;
}
