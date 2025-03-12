import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { Router } from '@angular/router';


@Component({
  selector: 'app-invoices-page',
  imports: [TableComponentComponent],
  templateUrl: './invoices-page.component.html',
  styleUrl: './invoices-page.component.scss'
})
export class InvoicesPageComponent {

  constructor (private router: Router) {}

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.customers = response
      },
      error: (error) => {
          if (error.status === 401) {
            this.router.navigate(['/login']);
          }
      }
    })
  }

}
