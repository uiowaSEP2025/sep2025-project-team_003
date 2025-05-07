import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { Router } from '@angular/router';
import { InvoiceService } from '../../services/invoice.service';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';

@Component({
  selector: 'app-invoices-page',
  imports: [
    TableComponentComponent,
    MatButtonModule,
    MatIconModule,
    LoadingFallbackComponent,
    PageTemplateComponent
  ],
  templateUrl: './invoices-page.component.html',
  styleUrl: './invoices-page.component.scss'
})
export class InvoicesPageComponent implements OnInit{
  invoiceService: InvoiceService


  constructor (private router: Router, invoiceService: InvoiceService) {
    this.invoiceService = invoiceService
  }

  invoices: any = null;

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.invoiceService.getInvoicesForOrganization({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.invoices = response
      },
      error: (error) => {
      }
    })
  }

  redirectInvoiceDetails(element: any) {
    this.router.navigate([`/invoice/${element.id}`])
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }

}
