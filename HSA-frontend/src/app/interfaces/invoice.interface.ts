export interface Invoice {
  invoiceID: number;
  customerID: number;
  customerName: string;
  invoiceDate: Date;
  invoiceDueDate: Date;
  invoiceStatus: string;
  invoicePrice: number;
  invoiceTax: number;

}
