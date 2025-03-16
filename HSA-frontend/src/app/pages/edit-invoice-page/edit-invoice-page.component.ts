import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { QuoteService } from '../../services/quote.service';
import { Router, ActivatedRoute } from '@angular/router';
import { OnInit } from '@angular/core';
import { MatError } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { ErrorHandlerService } from '../../services/error.handler.service';

@Component({
  selector: 'app-edit-invoice-page',
  imports: [TableComponentComponent,MatError, MatButtonModule],
  templateUrl: './edit-invoice-page.component.html',
  styleUrl: './edit-invoice-page.component.scss'
})
export class EditInvoicePageComponent implements OnInit{
  selectedQuotes: number[] = []
  quotes: any
  selectedQuotesIsError = false
  invoiceID!: number

  constructor (private router: Router, private quoteService:QuoteService, private activatedRoute: ActivatedRoute, private errorHandler: ErrorHandlerService ) {}

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe(params => {
      this.invoiceID = Number(params.get('id'));
    })
    this.loadQuotesToTable("", 5, 0);
  }

  setSelectedQuotes(newQuotes: number[]) {
    this.selectedQuotes = [...newQuotes ]
  }

  loadQuotesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.quoteService.getQuotesByInvoice(this.invoiceID, { search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.quotes = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })}

    onSubmit() {

    }


  
}
