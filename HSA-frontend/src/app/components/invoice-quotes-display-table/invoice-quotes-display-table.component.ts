import { Component, OnInit } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { Input } from '@angular/core';
import { InvoiceQuoteDisplayInterface } from '../../interfaces/invoice.quote.display.interface';

@Component({
  selector: 'app-invoice-quotes-display-table',
  imports: [MatTableModule],
  templateUrl: './invoice-quotes-display-table.component.html',
  styleUrl: './invoice-quotes-display-table.component.scss'
})
export class InvoiceQuotesDisplayTableComponent implements OnInit {
  @Input({ required: true }) dataSource!: InvoiceQuoteDisplayInterface[]
  quotes: any

  ngOnInit(): void {
    this.quotes = this.dataSource.map((quote: InvoiceQuoteDisplayInterface) => {
      return {
        "Material Subtotal": quote.materialSubtotal,
        "Total Price": quote.totalPrice,
        "Job Description": quote.jobDescription
      }
    })

    this.quotes.push(
      {
        "Material Subtotal": "",
        "Total Price": "",
        "Job Description": "Total"
      }

    )

    console.log(this.quotes)
  }

  displayedColumns = ["Job Description", "Material Subtotal", "Total Price"]

}
