import { Component, OnInit } from '@angular/core';
import { CustomerService } from '../../services/customer.service';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { QuoteService } from '../../services/quote.service';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatError } from '@angular/material/form-field';

@Component({
  selector: 'app-create-invoice-page',
  imports: [TableComponentComponent, CommonModule, MatButtonModule, MatError],
  templateUrl: './create-invoice-page.component.html',
  styleUrl: './create-invoice-page.component.scss'
})
export class CreateInvoicePageComponent implements OnInit {

  quotes: any
  customers: any
  selectedCustomers: any = []
  selectedCustomersIsError: boolean = false
  selectedQuotes: any = []
  selectedQuotesIsError: boolean = false

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
      },
      error: (error) => {
        if (error.status === 401) {
          this.router.navigate(['/login']);
        }
      }
    })
  }

  setSelectedQuotes(quotes: number[]) {
    this.selectedQuotes = [...quotes]
    this.selectedQuotesIsError = this.selectedQuotes.length === 0 ? true : false
  }

  setSelectedCustomers(cust: number[]) {
    this.selectedCustomers = [...cust]
    if (this.selectedCustomers.length !== 0) {
      this.selectedCustomersIsError = false
      this.selectedQuotes = []
      this.loadQuotesToTable('', 5, 0)
    }
    else {
      this.selectedCustomersIsError = true
    }
  }

  onSubmit() {}


}

