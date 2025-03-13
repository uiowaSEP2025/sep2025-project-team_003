import { Component } from '@angular/core';
import { InvoiceDataInterface } from '../../interfaces/api-responses/invoice.api.data.interface';

@Component({
  selector: 'app-view-invoice-page',
  imports: [],
  templateUrl: './view-invoice-page.component.html',
  styleUrl: './view-invoice-page.component.scss'
})
export class ViewInvoicePageComponent {
  invoiceData: null | InvoiceDataInterface = null;

}
