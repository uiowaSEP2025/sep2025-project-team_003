import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { CustomerService } from '../../../services/customer.service';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { CommonModule } from '@angular/common';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';

@Component({
  selector: 'app-customers-page',
  imports: [TableComponentComponent, MatButtonModule, MatIconModule, CommonModule, LoadingFallbackComponent],
  templateUrl: './customers-page.component.html',
  styleUrl: './customers-page.component.scss'
})

export class CustomersPageComponent implements OnInit {
  customers: any = null
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
          this.errorHandler.handleError(error, 'customers')
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
