import { Component } from '@angular/core';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { InvoiceService } from '../../services/invoice.service';
import { OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { InvoiceJobComponent } from '../../components/invoice-job/invoice-job.component';
import { Invoice } from '../../components/invoice-job/invoice-job.component';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';
@Component({
  selector: 'app-view-invoice-page',
  imports: [LoadingFallbackComponent, CommonModule, MatButtonModule, MatIconModule, InvoiceJobComponent, MatCardModule, PageTemplateComponent],
  templateUrl: './view-invoice-page.component.html',
  styleUrl: './view-invoice-page.component.scss'
})
export class ViewInvoicePageComponent implements OnInit{
  invoiceID!: number
  invoiceData: Invoice | null = null;

  constructor (private router: Router, private invoiceService: InvoiceService, private activatedRoute:ActivatedRoute) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.invoiceID = Number(params.get('id'));
    })
  }

  ngOnInit(): void {
    this.invoiceService.getSpecificInvoiceData(this.invoiceID).subscribe(
      {next: (response) => {
        this.invoiceData = response
        console.log(response)
      },
      error: (error) => {
      }}
    )

  }

  navigateViewInvoice() {
    window.open(`/api/generate/invoice/${this.invoiceID}`, '_blank');
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
