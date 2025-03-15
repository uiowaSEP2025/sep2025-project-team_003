import { Component } from '@angular/core';
import { InvoiceDataInterface } from '../../interfaces/api-responses/invoice.api.data.interface';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { InvoiceService } from '../../services/invoice.service';
import { OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { InvoiceQuotesDisplayTableComponent } from '../../components/invoice-quotes-display-table/invoice-quotes-display-table.component';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-view-invoice-page',
  imports: [LoadingFallbackComponent,CommonModule, MatButtonModule, MatIconModule, InvoiceQuotesDisplayTableComponent, MatCardModule],
  templateUrl: './view-invoice-page.component.html',
  styleUrl: './view-invoice-page.component.scss'
})
export class ViewInvoicePageComponent implements OnInit{
  invoiceID!: number
  invoiceData: InvoiceDataInterface | null = null;

  constructor (private invoiceService: InvoiceService, private activatedRoute:ActivatedRoute, private router: Router) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.invoiceID = Number(params.get('id'));
    })
  }

  ngOnInit(): void {
    this.invoiceService.getSpecificInvoiceData(this.invoiceID).subscribe(
      {next: (response) => {
        console.log(response)
        this.invoiceData = response
      },
      error: (error) => {
        if (error.status === 401) {
          this.router.navigate(['/login']);
        }
        if (error.status === 404) {
          this.router.navigate(['/404']);
        }
      }}
    )
    
  }



}
