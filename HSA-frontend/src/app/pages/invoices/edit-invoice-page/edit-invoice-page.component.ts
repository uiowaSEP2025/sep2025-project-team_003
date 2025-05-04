import { Component, inject } from '@angular/core';
import { TableComponentComponent } from '../../../components/table-component/table-component.component';
import { QuoteService } from '../../../services/quote.service';
import { ActivatedRoute } from '@angular/router';
import { OnInit } from '@angular/core';
import { MatError } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { FormGroup, FormControl, FormsModule } from '@angular/forms';
import { InvoiceDatePickerComponent } from '../../../components/invoice-date-picker/invoice-date-picker.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ViewChild } from '@angular/core';
import { InvoiceStateRegressionConfirmerComponent } from '../../../components/invoice-state-regression-confirmer/invoice-state-regression-confirmer.component';
import { MatDialog } from '@angular/material/dialog';
import { InvoiceService } from '../../../services/invoice.service';
import { StringFormatter } from '../../../utils/string-formatter';
import { Router } from '@angular/router';
import { Validators } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import integerValidator from '../../../utils/whole-number-validator';

export interface DateRange {
  issued: FormControl<Date | null>;
  due: FormControl<Date | null>;
}

@Component({
  selector: 'app-edit-invoice-page',
  imports: [MatError, MatButtonModule, MatSelectModule,
    FormsModule, MatInputModule, MatFormFieldModule, MatCardModule,
    InvoiceDatePickerComponent, ReactiveFormsModule],
  templateUrl: './edit-invoice-page.component.html',
  providers: [],
  standalone: true,
  styleUrl: './edit-invoice-page.component.scss'
})
export class EditInvoicePageComponent implements OnInit {
  selectedQuotes: number[] = []
  quotes: any
  selectedQuotesIsError = false
  invoiceID!: number
  customerName!: string
  dateIssued!: string
  dateDue!: string
  status!: 'issued' | 'created' | 'paid'// also serves as a form control
  initialStatus!: string
  taxPercent!: number
  paymentLink!: string;
  customerId!: number
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


  constructor(private quoteService: QuoteService, private activatedRoute: ActivatedRoute,
    private invoiceService: InvoiceService, private stringFormatter: StringFormatter,
    private router: Router) { }

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
      console.log(params)
      this.initialStatus = params['status'];
      this.status = params['status'];
      this.dateDue = params['date_due'];
      this.dateIssued = params['date_issued'];
      this.customerName = params['customer'];
      this.customerId = params['customer_id'];
      this.taxPercent = parseInt(this.fixBackendTaxPercentage(params['sales_tax_percent']));
      this.paymentLink = params['payment_link'];
    })
    this.taxAmount.setValue(this.taxPercent.toFixed(2))

    if (this.dateIssued !== "N/A") {
      const split =  this.dateIssued.split('-')
      const year = split[0]
      const month = split[1]
      const day = split[2]
      this.range.controls.issued.setValue(new Date(parseInt(year), parseInt(month) - 1, parseInt(day)))
    }

    if (this.dateDue !== "N/A") {
      const split =  this.dateDue.split('-')
      const year = split[0]
      const month = split[1]
      const day = split[2]
      this.range.controls.due.setValue(new Date(parseInt(year), parseInt(month) - 1, parseInt(day)))
    }
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(InvoiceStateRegressionConfirmerComponent,
      {data: this.initialStatus}
    );

    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        const data = {
          quoteIDs: this.selectedQuotes,
          status: this.status,
          dateIssued: this.stringFormatter.dateFormatter(this.range.controls.issued.value),
          dateDue: this.stringFormatter.dateFormatter(this.range.controls.due.value),
          taxPercent: this.taxAmount.value.toString(),
          customerId: this.customerId,
          paymentLink: this.paymentLink,
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



  onSubmit() {
    if (!this.taxAmount.valid) {
      return;
    }
    if (this.isDateSelectVisible() && !this.datePicker.validate()) {
      this.selectedQuotesIsError = false;
      return false;
    }
    this.selectedQuotesIsError = false;
    if (this.initialStatus === 'issued' || this.initialStatus === 'paid') {
      this.openDialog()
      return;
    }

    const data = {
      quoteIDs: this.selectedQuotes,
      status: this.status,
      dateIssued: this.stringFormatter.dateFormatter(this.range.controls.issued.value) ,
      dateDue: this.stringFormatter.dateFormatter(this.range.controls.due.value),
      taxPercent: this.taxAmount.value.toString(),
      customerId: this.customerId,
      paymentLink: this.paymentLink,
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
