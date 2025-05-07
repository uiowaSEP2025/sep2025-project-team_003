import { Component, OnInit } from '@angular/core';
import { CustomerService } from '../../services/customer.service';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatError } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { InvoiceService } from '../../services/invoice.service';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { InvoiceDatePickerComponent } from '../../components/invoice-date-picker/invoice-date-picker.component';
import { DateRange } from '../edit-invoice-page/edit-invoice-page.component';
import { FormGroup, FormControl } from '@angular/forms';
import { MatLabel } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ViewChild } from '@angular/core';
import { StringFormatter } from '../../utils/string-formatter';
import { Validators } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import { ReactiveFormsModule } from '@angular/forms';
import integerValidator from '../../utils/whole-number-validator';
import { JobService } from '../../services/job.service';
import { OrganizationService } from '../../services/organization.service';

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
  jobs: any
  customers: any
  selectedCustomers: any = []
  selectedCustomersIsError: boolean = false
  selectedJobs: any = []
  selectedJobsIsError: boolean = false
  orgHasLink: boolean | null = null
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

  constructor(private customerService: CustomerService, private router: Router,
    private invoiceService: InvoiceService, private stringFormatter: StringFormatter,
    private jobService: JobService, private orgService: OrganizationService) { }

  ngOnInit(): void {
    this.loadCustomersToTable("", 5, 0);
    this.orgService.getPayemntLink().subscribe({
      next: (response) => {
        this.orgHasLink = response.URL !== null
        console.log(this.orgHasLink)
      },
      error: () => {}
    })

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

  loadJobsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.jobService.getInvoicableJobs(this.selectedCustomers[0], searchTerm, pageSize, offSet).subscribe({
      next: (response) => {
        this.jobs = response
      },
      error: (error) => {
      }
    })
  }

  setSelectedQuotes(jobs: number[]) {
    this.selectedJobs = [...jobs]
    this.selectedJobsIsError = this.selectedJobs.length === 0 ? true : false
  }

  setSelectedCustomers(cust: number[]) {
    this.selectedCustomers = [...cust]
    if (this.selectedCustomers.length !== 0) {
      this.selectedCustomersIsError = false
      this.selectedJobs = []
      this.selectedJobsIsError = false
      this.loadJobsToTable('', 5, 0)
    }
    else {
      this.selectedJobs = []
      this.jobs = { data: [], totalCount: 0 }
      this.selectedCustomersIsError = true
    }
  }

  onSubmit() {
    let haserror: boolean = false
    if (this.isDateSelectVisible()) {
      haserror = !this.datePicker.validate()
    }
    if (this.selectedCustomers.length === 0) {
      this.selectedCustomersIsError = true
      haserror = true;
    }
    if (this.selectedJobs.length === 0) {
      const jobsTableVisible = this.selectedCustomers.length !== 0
      if (jobsTableVisible) {
        this.selectedJobsIsError = true
        haserror = true;
      }
    }
    this.taxAmount.markAsUntouched()
    if (!this.taxAmount.valid) {
      this.taxAmount.markAsTouched()
      haserror = true;
    }
    if (haserror) {
      return;
    }
    const json = {
      customerID: this.selectedCustomers[0],
      jobIds: this.selectedJobs,
      status: this.status,
      issuedDate: this.stringFormatter.dateFormatter(this.range.controls.issued.value),
      dueDate: this.stringFormatter.dateFormatter(this.range.controls.due.value),
      tax: this.taxAmount.value.toString()
    }
    this.invoiceService.createInvoice(json).subscribe(
      {
        next: (response) => {
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

