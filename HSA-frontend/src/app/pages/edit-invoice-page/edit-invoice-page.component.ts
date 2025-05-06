import { Component, inject } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { ActivatedRoute } from '@angular/router';
import { OnInit } from '@angular/core';
import { MatError } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { FormGroup, FormControl, FormsModule } from '@angular/forms';
import { InvoiceDatePickerComponent } from '../../components/invoice-date-picker/invoice-date-picker.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ViewChild } from '@angular/core';
import { InvoiceStateRegressionConfirmerComponent } from '../../components/invoice-state-regression-confirmer/invoice-state-regression-confirmer.component';
import { MatDialog } from '@angular/material/dialog';
import { InvoiceService } from '../../services/invoice.service';
import { StringFormatter } from '../../utils/string-formatter';
import { Router } from '@angular/router';
import { Validators } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import integerValidator from '../../utils/whole-number-validator';
import { JobService } from '../../services/job.service';

export interface DateRange {
  issued: FormControl<Date | null>;
  due: FormControl<Date | null>;
}

@Component({
  selector: 'app-edit-invoice-page',
  imports: [TableComponentComponent, MatError, MatButtonModule, MatSelectModule,
    FormsModule, MatInputModule, MatFormFieldModule, MatCardModule,
    InvoiceDatePickerComponent, ReactiveFormsModule],
  templateUrl: './edit-invoice-page.component.html',
  providers: [],
  styleUrl: './edit-invoice-page.component.scss'
})
export class EditInvoicePageComponent implements OnInit {
  selectedJobs: number[] = []
  jobs: any
  selectedJobsisError = false
  invoiceID!: number
  customerName!: string
  issuanceDate!: string
  dueDate!: string
  status!: 'issued' | 'created' | 'paid'// also serves as a form control
  initialStatus!: string
  tax!: number
  isFirstLoad = true

  readonly range: FormGroup<DateRange> = new FormGroup({
    issued: new FormControl<Date | null>(null),
    due: new FormControl<Date | null>(null),
  });

  isDateSelectVisible = () => (!(this.status === 'created'))
  @ViewChild(InvoiceDatePickerComponent) datePicker!: InvoiceDatePickerComponent;
  readonly dialog = inject(MatDialog);
    taxAmount: FormControl = new FormControl('', [Validators.required,  Validators.min(0),
      Validators.min(0), Validators.max(100), integerValidator
    ])

    matcher = new GenericFormErrorStateMatcher()
  
  
  constructor(private activatedRoute: ActivatedRoute, 
    private invoiceService: InvoiceService, private stringFormatter: StringFormatter, 
    private router: Router, private JobsService: JobService) { }

    private fixBackendTaxPercentage(tax: string): string {
      if (tax === "1.00") {
        return "100"
      }
      tax = tax.split('.')[1]
      return tax
    }

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe(params => {
      this.invoiceID = Number(params.get('id'));
    })

    this.activatedRoute.queryParams.subscribe(params => {
      this.initialStatus = params['status'];
      this.status = params['status'];
      this.dueDate = params['due_date'];
      this.issuanceDate = params['issuance_date'];
      this.customerName = params['customer'];
      this.tax = parseInt(this.fixBackendTaxPercentage(params['tax']));
    })
    this.taxAmount.setValue(this.tax.toFixed(2))

    if (this.issuanceDate !== "N/A") {
      const split =  this.issuanceDate.split('-')
      const year = split[0]
      const month = split[1]
      const day = split[2]
      this.range.controls.issued.setValue(new Date(parseInt(year), parseInt(month) - 1, parseInt(day)))
    }

    if (this.dueDate !== "N/A") {
      const split =  this.dueDate.split('-')
      const year = split[0]
      const month = split[1]
      const day = split[2]
      this.range.controls.due.setValue(new Date(parseInt(year), parseInt(month) - 1, parseInt(day)))
    }
    this.loadJobs("", 5, 0);    
  }

  setSelectedJobs(selectedJobs: number[]) {
    if (selectedJobs.length === 0) {
      this.selectedJobsisError = true
      this.selectedJobs = [...selectedJobs]
    }
    else {
      this.selectedJobsisError = false
      this.selectedJobs = [...selectedJobs]
    }

  }

  openDialog(): void {
    const dialogRef = this.dialog.open(InvoiceStateRegressionConfirmerComponent,
      {data: this.initialStatus}
    );

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        const data = {
          quoteIDs: this.selectedJobs,
          status: this.status,
          issuedDate: this.stringFormatter.dateFormatter(this.range.controls.issued.value),
          dueDate: this.stringFormatter.dateFormatter(this.range.controls.due.value),
          tax: this.taxAmount.value.toString()
        }
        this.invoiceService.updateInvoice(this.invoiceID, data).subscribe(
          {next: (response) => {
            this.router.navigate(['/invoices']);
          },
          error: (error) => {
          }})
      }
    });
  }


  loadJobs(searchTerm: string, pageSize: number, offSet: number) {
      this.JobsService.getJobsByInvoice(this.invoiceID, searchTerm, pageSize, offSet).subscribe({
        next: (response) => {
          
          if (this.isFirstLoad) {
            this.isFirstLoad = false
            const ids = response.data.filter((job: any) => (job.invoice===this.invoiceID)).map((job:any) => (job.id))
            this.setSelectedJobs(ids)
          }
          this.jobs = response
        },
        error: () => {}
      })
  }

  onSubmit() {
    if (!this.taxAmount.valid) {
      return;
    }
    if (this.selectedJobs.length === 0) {
      this.datePicker?.validate()
      this.selectedJobsisError = true;
      return;
    }
    if (this.isDateSelectVisible() && !this.datePicker.validate()) {
      this.selectedJobsisError = false;
      return false;
    }
    this.selectedJobsisError = false;
    if (this.initialStatus === 'issued' || this.initialStatus === 'paid') {
      this.openDialog()
      return;
    }
    
    const data = {
      quoteIDs: this.selectedJobs,
      status: this.status,
      issuedDate: this.stringFormatter.dateFormatter(this.range.controls.issued.value) ,
      dueDate: this.stringFormatter.dateFormatter(this.range.controls.due.value),
      tax: this.taxAmount.value.toString()
    }
    this.invoiceService.updateInvoice(this.invoiceID, data).subscribe(
      {next: (response) => {
        this.router.navigate(['/invoices']);
      },
      error: (error) => {
      }})
      return;
  }
}
