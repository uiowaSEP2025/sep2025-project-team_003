import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { QuoteService } from '../../services/quote.service';
import { Router, ActivatedRoute } from '@angular/router';
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
  status!: string
  readonly range = new FormGroup({
    start: new FormControl<Date | null>(null),
    end: new FormControl<Date | null>(null),
  });
  @ViewChild(InvoiceDatePickerComponent) datePicker!: InvoiceDatePickerComponent;

  constructor(private router: Router, private quoteService: QuoteService, private activatedRoute: ActivatedRoute, private errorHandler: ErrorHandlerService) { }

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe(params => {
      this.invoiceID = Number(params.get('id'));
    })

    this.activatedRoute.queryParams.subscribe(params => {
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
    if (this.selectedQuotes.length === 0 || !this.datePicker.validate()) {
      return;
    }
  }
}
