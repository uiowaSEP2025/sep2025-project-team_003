import { Component } from '@angular/core';
import { InvoiceDataInterface } from '../../interfaces/api-responses/invoice.api.data.interface';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { InvoiceService } from '../../services/invoice.service';
import { OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-view-invoice-page',
  imports: [LoadingFallbackComponent,CommonModule],
  templateUrl: './view-invoice-page.component.html',
  styleUrl: './view-invoice-page.component.scss'
})
export class ViewInvoicePageComponent implements OnInit{
  invoiceID!: number
  invoiceData: null | InvoiceDataInterface = null;

  constructor (private invoiceService: InvoiceService, private activatedRoute:ActivatedRoute, private router: Router) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.invoiceID = Number(params.get('id'));
    })
  }

  ngOnInit(): void {
    this.invoiceService.getSpecificInvoiceData(this.invoiceID).subscribe(
      {next: (response) => {
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
