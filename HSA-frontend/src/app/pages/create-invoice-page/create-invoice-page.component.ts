import { Component, OnInit } from '@angular/core';
import { CustomerService } from '../../services/customer.service';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { QuoteService } from '../../services/quote.service';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-create-invoice-page',
  imports: [TableComponentComponent, CommonModule, MatButtonModule],
  templateUrl: './create-invoice-page.component.html',
  styleUrl: './create-invoice-page.component.scss'
})
export class CreateInvoicePageComponent implements OnInit {

  quotes: any
  customers: any
  selectedCustomers: any = []
  selectedQuotes: any = []

  constructor(private customerService: CustomerService, private router: Router, private quoteService: QuoteService) { }

  ngOnInit(): void {
    this.loadCustomersToTable("", 5, 0);
  }



  loadCustomersToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
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


  loadQuotesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.quoteService.getQuotesByCustomer(this.selectedCustomers[0], { search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.quotes = response
        console.log(this.quotes)
      },
      error: (error) => {
        if (error.status === 401) {
          this.router.navigate(['/login']);
        }
      }
    })
  }

  setSelectedCustomers(cust: number[]) {
    this.selectedCustomers = [...cust]
    if (this.selectedCustomers.length !== 0) {
      this.loadQuotesToTable('', 5, 0)
    }
  }

  onSubmit() {}


}

