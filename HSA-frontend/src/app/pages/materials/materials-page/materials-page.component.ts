import { Component, OnInit, ViewChild } from '@angular/core';
import {TableComponentComponent} from '../../../components/table-component/table-component.component';
import { MaterialService } from '../../../services/material.service';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { CommonModule } from '@angular/common';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';
import {PageTemplateComponent} from "../../../components/page-template/page-template.component";
import {Material} from '../../../interfaces/material.interface';
import {TableApiResponse} from '../../../interfaces/api-responses/table.api.interface';

@Component({
  selector: 'app-materials-page',
    imports: [
        TableComponentComponent,
        CommonModule,
        LoadingFallbackComponent,
        PageTemplateComponent
    ],
  templateUrl: './materials-page.component.html',
  styleUrl: './materials-page.component.scss'
})
export class MaterialsPageComponent implements OnInit {
  loading = false;
  materials: TableApiResponse<Material> = {data: [], totalCount: 0}
  materialService: MaterialService
  @ViewChild(TableComponentComponent) tableComponent!: TableComponentComponent

  constructor(materialService: MaterialService, private errorHandler: ErrorHandlerService) {
    this.materialService = materialService
  }

  ngOnInit(): void {
    void this.loadDataToTable("", 5, 0);
  }

  async loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.loading = true;
    this.materialService.getMaterial({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.materials = response
        console.log(response)
        this.loading = false;
      },
      error: (error) => {
        this.errorHandler.handleError(error, 'materials')
        this.loading = false;
      }
    })

  }
}
