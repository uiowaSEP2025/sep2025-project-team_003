import { Component, OnInit } from '@angular/core';
import {TableComponentComponent} from '../../../components/table-component/table-component.component';
import { ServiceService } from '../../../services/service.service';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { CommonModule } from '@angular/common';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';
import {PageTemplateComponent} from "../../../components/page-template/page-template.component";
import {TableApiResponse} from '../../../interfaces/api-responses/table.api.interface';
import {Service} from '../../../interfaces/service.interface';

@Component({
  selector: 'app-service-page',
    imports: [
        TableComponentComponent,
        CommonModule,
        LoadingFallbackComponent,
        PageTemplateComponent
    ],
  templateUrl: './service-page.component.html',
  styleUrl: './service-page.component.scss'
})
export class ServicePageComponent implements OnInit {
  loading = false;
  services: TableApiResponse<Service> = {data: [], totalCount: 0};
  serviceService: ServiceService

  constructor(serviceService: ServiceService, private errorHandler: ErrorHandlerService) {
    this.serviceService = serviceService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  async loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.loading = true;
    this.serviceService.getService({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.services = response
        this.loading = false;
      },
      error: (error) => {
        this.errorHandler.handleError(error, 'services')
        this.loading = false;
      }
    })
  }

}
