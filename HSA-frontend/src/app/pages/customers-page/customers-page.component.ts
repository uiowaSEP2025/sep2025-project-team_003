import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
import { CommonModule } from '@angular/common';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

@Component({
  selector: 'app-customers-page',
  imports: [TableComponentComponent, MatButtonModule, MatIconModule, CommonModule, LoadingFallbackComponent, PageTemplateComponent],
  templateUrl: './customers-page.component.html',
  styleUrl: './customers-page.component.scss'
})

export class CustomersPageComponent implements OnInit {
  customers: any = null
  customerService: CustomerService

  constructor(private router: Router, customerService: CustomerService, private breakpointObserver: BreakpointObserver) {
    this.customerService = customerService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
    this.breakpointObserver.observe([Breakpoints.Handset]).subscribe(result => {});
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.customers = response
      },
      error: (error) => {
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
