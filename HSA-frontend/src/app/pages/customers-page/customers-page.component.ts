import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
<<<<<<< HEAD
=======
import { ErrorHandlerService } from '../../services/error.handler.service';
>>>>>>> 4a1ec86876bccea3be7a144da379d86a255e706a

@Component({
  selector: 'app-customers-page',
  imports: [TableComponentComponent, MatButtonModule, MatIconModule],
  templateUrl: './customers-page.component.html',
  styleUrl: './customers-page.component.scss'
})

export class CustomersPageComponent implements OnInit {
  customers: any
  customerService: CustomerService

  constructor(private router: Router, customerService: CustomerService, private errorHandler: ErrorHandlerService) {
    this.customerService = customerService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.customers = response
      },
      error: (error) => {
          this.errorHandler.handleError(error)
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
