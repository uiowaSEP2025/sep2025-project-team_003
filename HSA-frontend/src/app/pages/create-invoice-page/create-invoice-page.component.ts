import { Component, OnInit } from '@angular/core';
import { CustomerService } from '../../services/customer.service';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../components/table-component/table-component.component';

@Component({
  selector: 'app-create-invoice-page',
  imports: [TableComponentComponent],
  templateUrl: './create-invoice-page.component.html',
  styleUrl: './create-invoice-page.component.scss'
})
export class CreateInvoicePageComponent implements OnInit{

  quotes: any
  customers: any
  selectedCustomers: any = []
  constructor (private customerService: CustomerService, private router: Router) {}
  
  ngOnInit(): void {
    this.loadCustomersToTable("", 5, 0);
  }

  setSelectedCustomers(cust: number[]) {
    this.selectedCustomers = [...cust]
  }

  loadCustomersToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.customers = response
        console.log(this.customers)
      },
      error: (error) => {
          if (error.status === 401) {
            this.router.navigate(['/login']);
          }
      }
    })
  }
  

}
