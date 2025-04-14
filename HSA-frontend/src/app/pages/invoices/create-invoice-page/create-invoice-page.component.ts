import { Component, OnInit } from '@angular/core';
import { CustomerService } from '../../../services/customer.service';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../../components/table-component/table-component.component';
import { QuoteService } from '../../../services/quote.service';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatError } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { InvoiceService } from '../../../services/invoice.service';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { InvoiceDatePickerComponent } from '../../../components/invoice-date-picker/invoice-date-picker.component';
import { DateRange } from '../edit-invoice-page/edit-invoice-page.component';
import { FormGroup, FormControl } from '@angular/forms';
import { MatLabel } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ViewChild } from '@angular/core';
import { StringFormatter } from '../../../utils/string-formatter';
import { Validators } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import { ReactiveFormsModule } from '@angular/forms';
import integerValidator from '../../../utils/whole-number-validator';

@Component({
  selector: 'app-create-invoice-page',
  imports: [TableComponentComponent, CommonModule, MatButtonModule, MatError,
    FormsModule, MatFormFieldModule, InvoiceDatePickerComponent, MatSelectModule,
    MatLabel, MatInputModule, ReactiveFormsModule
  ],
  templateUrl: './create-invoice-page.component.html',
  styleUrl: './create-invoice-page.component.scss'
})
export class CreateInvoicePageComponent implements OnInit {
  quotes: any
  customers: any
  selectedCustomers: any = []
  selectedCustomersIsError = false
  selectedQuotes: any = []
  selectedQuotesIsError = false
  status: 'created' | 'issued' | 'paid' = 'created'
  matcher = new GenericFormErrorStateMatcher()
  @ViewChild(InvoiceDatePickerComponent) datePicker!: InvoiceDatePickerComponent;

  readonly range: FormGroup<DateRange> = new FormGroup({
    issued: new FormControl<Date | null>(null),
    due: new FormControl<Date | null>(null),
  });

  taxAmount: FormControl = new FormControl('', [Validators.required,  Validators.min(0),
    Validators.min(0), Validators.max(100), integerValidator
  ])

  constructor(private customerService: CustomerService, private router: Router, private quoteService: QuoteService,
    private invoiceService: InvoiceService, private stringFormatter: StringFormatter) { }

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
      }
    })
  }

  loadQuotesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.quoteService.getQuotesByCustomer(this.selectedCustomers[0], { search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.quotes = response
      },
      error: (error) => {
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
      this.quotes = { data: [], totalCount: 0 }
      this.selectedCustomersIsError = true
    }
  }

  onSubmit() {
    let validDates: any
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
    if (!this.taxAmount.valid) {
      return;
    }
    if (this.isDateSelectVisible() && !validDates) {
      return;
    }
    const json = {
      status: this.status,
      issuance_date: new Date,
      due_date: new Date,
      tax: this.taxAmount.value,
      customer: {
        customerID: 0,
        organizationID: 0,
        notes: '',
        firstName: '',
        lastName: '',
        email: '',
        phone: ''
      },
      jobs: [],
      discounts: []
    }
    this.invoiceService.createInvoice(json).subscribe(
      {
        next: () => {
          this.router.navigate(['/invoices']);
        },
        error: (error) => {
        }
      }
    )
    return;
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}

