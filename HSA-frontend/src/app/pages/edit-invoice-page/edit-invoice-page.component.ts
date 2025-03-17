import { Component, inject } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { QuoteService } from '../../services/quote.service';
import { ActivatedRoute } from '@angular/router';
import { OnInit } from '@angular/core';
import { MatError } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { ErrorHandlerService } from '../../services/error.handler.service';
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
  selectedQuotes: number[] = []
  quotes: any
  selectedQuotesIsError = false
  invoiceID!: number
  customerName!: string
  issuanceDate!: string
  dueDate!: string
  status!: string // also serves as a form control
  initialStatus!: string
  readonly range: FormGroup<DateRange> = new FormGroup({
    issued: new FormControl<Date | null>(null),
    due: new FormControl<Date | null>(null),
  });

  isDateSelectVisible = () => (!(this.status === 'created'))
  @ViewChild(InvoiceDatePickerComponent) datePicker!: InvoiceDatePickerComponent;
  readonly dialog = inject(MatDialog);

  
  constructor(private quoteService: QuoteService, private activatedRoute: ActivatedRoute, private errorHandler: ErrorHandlerService) { }

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
    })
    this.loadQuotesToTable("", 5, 0);
  }

  setSelectedQuotes(newQuotes: number[]) {
    if (newQuotes.length === 0) {
      this.selectedQuotesIsError = true
      this.selectedQuotes = [...newQuotes]
    }
    else {
      this.selectedQuotesIsError = false
      this.selectedQuotes = [...newQuotes]
    }

  }

  openDialog(): void {
    const dialogRef = this.dialog.open(InvoiceStateRegressionConfirmerComponent,
      {data: this.initialStatus}
    );
    dialogRef.afterClosed().subscribe(result => {
      if (result === true) {
        
      }
    });
  }


  loadQuotesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.quoteService.getQuotesByInvoice(this.invoiceID, { search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.quotes = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  onSubmit() {
    console.log(this.isDateSelectVisible)
    if (this.selectedQuotes.length === 0) {
      this.datePicker.validate()
      this.selectedQuotesIsError = true;
      return;
    }
    if (this.isDateSelectVisible() && !this.datePicker.validate()) {
      this.selectedQuotesIsError = false;
      return false;
    }
    this.selectedQuotesIsError = false;
    if (this.initialStatus === 'issued' || this.initialStatus === 'paid') {
      this.openDialog()
    }
    return;
  }
}
