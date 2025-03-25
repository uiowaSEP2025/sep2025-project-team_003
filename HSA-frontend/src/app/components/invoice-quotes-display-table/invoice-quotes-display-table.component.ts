import { Component, OnInit } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { Input } from '@angular/core';
import { InvoiceQuoteDisplayInterface } from '../../interfaces/api-responses/invoice.quote.display.interface';
import { QuoteJSON } from '../../interfaces/api-responses/invoice.quote.display.interface';
import { StringFormatter } from '../../utils/string-formatter';

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

  constructor (private stringFormatter: StringFormatter) {}

  ngOnInit(): void {
    this.displayQuotes = this.dataSource.quotes.map(
      (quote) => ({
        "Material Subtotal": this.stringFormatter.formatCurrency(quote.materialSubtotal),
        "Total Price": this.stringFormatter.formatCurrency(quote.totalPrice),
        "Job Description": quote.jobDescription
      })
    )

    const totalMaterialSubtotal = this.stringFormatter.formatCurrency(this.dataSource.totalMaterialSubtotal)
    const totalPrice = this.stringFormatter.formatCurrency(this.dataSource.subtotal)
    this.displayQuotes.push({
      "Material Subtotal": `${totalMaterialSubtotal}`,
      "Total Price": `${totalPrice}`,
      "Job Description": "Subtotal:" 
    })

    const discountPercent = this.stringFormatter.formatPercent(this.dataSource.totalDiscount)
    this.displayQuotes.push({
      "Material Subtotal": "",
      "Total Price": `${discountPercent}`,
      "Job Description": "Discount:"
    })

    const taxPercent = this.stringFormatter.formatTaxPercent(this.dataSource.taxPercent)
    this.displayQuotes.push({
      "Material Subtotal": "",
      "Total Price": `${taxPercent}`,
      "Job Description": "Tax:"
    })

    const grandTotal = this.stringFormatter.formatCurrency(this.dataSource.grandtotal)
    this.displayQuotes.push({
      "Material Subtotal": "",
      "Total Price": `${grandTotal}`,
      "Job Description": "Total:"
    })
  }

  displayedColumns = ["Job Description", "Material Subtotal", "Total Price"]

}
