export interface Invoice {
  invoiceID: number;
  customerID: number;
  invoiceDate: Date;
  invoiceDueDate: Date;
  invoiceStatus: string;
  invoicePrice: number;
}
