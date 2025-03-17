import { Component, OnInit } from '@angular/core';
import { CustomerService } from '../../services/customer.service';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { QuoteService } from '../../services/quote.service';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatError } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { InvoiceService } from '../../services/invoice.service';
import { ErrorHandlerService } from '../../services/error.handler.service';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { InvoiceDatePickerComponent } from '../../components/invoice-date-picker/invoice-date-picker.component';
import { DateRange } from '../edit-invoice-page/edit-invoice-page.component';
import { FormGroup, FormControl } from '@angular/forms';
import { MatLabel } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ViewChild } from '@angular/core';
import { StringFormatter } from '../../utils/string-formatter';

@Component({
  selector: 'app-create-invoice-page',
  imports: [TableComponentComponent, CommonModule, MatButtonModule, MatError, 
    FormsModule, MatFormFieldModule, InvoiceDatePickerComponent, MatSelectModule,
    MatLabel,MatInputModule
  ],
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
  status: 'created' | 'issued' | 'paid' = 'created'
  @ViewChild(InvoiceDatePickerComponent) datePicker!: InvoiceDatePickerComponent;

  readonly range: FormGroup<DateRange> = new FormGroup({
      issued: new FormControl<Date | null>(null),
      due: new FormControl<Date | null>(null),
    });

  constructor(private customerService: CustomerService, private router: Router, private quoteService: QuoteService, 
    private invoiceService: InvoiceService, private errorHandler: ErrorHandlerService,
    private stringFormatter: StringFormatter) { }

  ngOnInit(): void {
    this.loadCustomersToTable("", 5, 0);
  }

  isDateSelectVisible = () => (!(this.status === 'created'))

  loadCustomersToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.customers = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  loadQuotesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.quoteService.getQuotesByCustomer(this.selectedCustomers[0], { search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.quotes = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
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
      this.selectedQuotesIsError = false
      this.loadQuotesToTable('', 5, 0)
    }
    else {
      this.selectedQuotes = []
      this.quotes = {data: [], totalCount: 0}
      this.selectedCustomersIsError = true
    }
  }

  onSubmit() {
    console.log('called')
    let validDates:any
    if (this.isDateSelectVisible()) {
      validDates = this.datePicker.validate()
    }
    if (this.selectedCustomers.length === 0) {
      this.selectedCustomersIsError = true
      return;
    }
    if (this.selectedQuotes.length === 0) {
      const quotesTableVisible = this.selectedCustomers.length !== 0
      if (quotesTableVisible) {
        this.selectedQuotesIsError = true
      }
      return;
    }
    if (this.isDateSelectVisible() && !validDates) {
      return;
    }

    const json = {
      customerID: this.selectedCustomers[0],
      quoteIDs: this.selectedQuotes,
      status: this.status,
      issuedDate: this.stringFormatter.dateFormatter(this.range.controls.issued.value) ,
      dueDate: this.stringFormatter.dateFormatter(this.range.controls.due.value)
    }
    this.invoiceService.createInvoice(json).subscribe(
      {next: (response) => {
        this.router.navigate(['/invoices']);
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }}
    )
    return;
  }


}

