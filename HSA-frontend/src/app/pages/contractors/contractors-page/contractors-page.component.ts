import {Component, OnInit} from '@angular/core';
import { TableComponentComponent } from '../../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import {Router} from '@angular/router';
import { ContractorService } from '../../../services/contractor.service';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { CommonModule } from '@angular/common';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';
import {PageTemplateComponent} from '../../../components/page-template/page-template.component';

@Component({
  selector: 'app-contractors-page',
  imports: [TableComponentComponent, MatButtonModule, CommonModule, LoadingFallbackComponent, PageTemplateComponent],
  templateUrl: './contractors-page.component.html',
  styleUrl: './contractors-page.component.scss'
})
export class ContractorsPageComponent implements OnInit  {
  contractors: any = null
  contractorService: ContractorService

  constructor(private router: Router, contractorService: ContractorService, private errorHandler: ErrorHandlerService) {
    this.contractorService = contractorService;
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.contractorService.getContractor({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.contractors = response
      },
      error: (error) => {
        this.errorHandler.handleError(error, 'contractors')
      }
    })
  }
}
