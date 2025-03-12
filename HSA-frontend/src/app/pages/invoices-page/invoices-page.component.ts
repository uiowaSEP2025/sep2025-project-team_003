import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { Router } from '@angular/router';
import { InvoiceService } from '../../services/invoice.service';


@Component({
  selector: 'app-invoices-page',
  imports: [TableComponentComponent],
  templateUrl: './invoices-page.component.html',
  styleUrl: './invoices-page.component.scss'
})
export class InvoicesPageComponent {

  constructor (private router: Router, private invoiceService: InvoiceService) {}

  invoices: any

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.invoiceService.getInvoicesForOrganization({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.invoices = response
      },
      error: (error) => {
          if (error.status === 401) {
            this.router.navigate(['/login']);
          }
      }
    })
  }

}
