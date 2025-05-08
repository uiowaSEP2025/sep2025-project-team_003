import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import { Router } from '@angular/router';
import { ContractorService } from '../../services/contractor.service';
import { CommonModule } from '@angular/common';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

@Component({
  selector: 'app-contractors-page',
  imports: [TableComponentComponent, MatButtonModule, MatIcon, CommonModule, LoadingFallbackComponent, PageTemplateComponent],
  templateUrl: './contractors-page.component.html',
  styleUrl: './contractors-page.component.scss'
})
export class ContractorsPageComponent implements OnInit  {
  contractors: any = null
  contractorService: ContractorService

  constructor(private router: Router, contractorService: ContractorService, private breakpointObserver: BreakpointObserver) {
    this.contractorService = contractorService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
    this.breakpointObserver.observe([Breakpoints.Handset]).subscribe(result => {});
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.contractorService.getContractor({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.contractors = response
      },
      error: (error) => {
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
