import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
import { TableApiResponse } from '../../interfaces/table.api.interface';
import { Customer } from '../../interfaces/customer.interface';


@Component({
  selector: 'app-customers-page',
  imports: [TableComponentComponent, MatButtonModule, MatIconModule],
  templateUrl: './customers-page.component.html',
  styleUrl: './customers-page.component.scss'
})
export class CustomersPageComponent {
  customerService: CustomerService
  custommer: TableApiResponse<Customer>

  constructor(private router: Router, customerService: CustomerService) {
    this.customerService = customerService
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.materials = response
      },
      error: (error) => {
        
      }
    })
  }

  onPageChange(event: { searchTerm: string; pageSize: number; offset: number }): void {
    this.loadDataToTable(event.searchTerm, event.pageSize, event.offset);
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
