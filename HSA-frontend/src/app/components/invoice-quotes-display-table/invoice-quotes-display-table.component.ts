import { Component, OnInit } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { Input } from '@angular/core';
import { InvoiceQuoteDisplayInterface } from '../../interfaces/api-responses/invoice.quote.display.interface';
import { QuoteJSON } from '../../interfaces/api-responses/invoice.quote.display.interface';

interface RowItem {
  "Material Subtotal": string,
  "Total Price": string,
  "Job Description": string
}

@Component({
  selector: 'app-invoice-quotes-display-table',
  imports: [MatTableModule],
  templateUrl: './invoice-quotes-display-table.component.html',
  styleUrl: './invoice-quotes-display-table.component.scss'
})
export class InvoiceQuotesDisplayTableComponent implements OnInit {
  @Input({ required: true }) dataSource!: InvoiceQuoteDisplayInterface
  quotes!: QuoteJSON[]
  displayQuotes!: RowItem[]

  ngOnInit(): void {
    this.displayQuotes = this.dataSource.quotes.map(
      (quote) => ({
        "Material Subtotal": quote.materialSubtotal,
        "Total Price": quote.materialSubtotal,
        "Job Description": quote.jobDescription
      })
    )

    const totalMaterialSubtotal = this.dataSource.totalMaterialSubtotal
    const totalPrice = this.dataSource.totalPrice

    this.displayQuotes.push({
      "Material Subtotal": `${totalMaterialSubtotal}`,
      "Total Price": `${totalPrice}`,
      "Job Description": "Total:" 
    })


    console.log(this.quotes)
  }

  displayedColumns = ["Job Description", "Material Subtotal", "Total Price"]

}
