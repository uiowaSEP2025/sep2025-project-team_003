import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { JobService } from '../../../services/job.service';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import {PageTemplateComponent} from '../../../components/page-template/page-template.component';
import {Job} from '../../../interfaces/job.interface';
import {TableApiResponse} from '../../../interfaces/api-responses/table.api.interface';

@Component({
  selector: 'app-job-page',
  imports: [TableComponentComponent, MatButtonModule, MatIconModule, LoadingFallbackComponent, CommonModule, PageTemplateComponent],
  templateUrl: './job-page.component.html',
  styleUrl: './job-page.component.scss'
})
export class JobPageComponent implements OnInit  {
  jobs: TableApiResponse<Job> = {
    data: [],
    totalCount: 0
  };
  loading = false;
  jobService: JobService

  constructor(private router: Router, jobService: JobService, private errorHandler: ErrorHandlerService) {
    this.jobService = jobService
  }

  ngOnInit(): void {
    void this.loadDataToTable("", 5, 0);
  }

  async loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.loading = true;
    this.jobService.getJob({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.jobs = response;
        this.loading = false;
      },
      error: (error) => {
        this.errorHandler.handleError(error, 'jobs');
        this.loading = false;
      }
    })
  }

  redirectJobDetails(element: any) {
    this.router.navigate([`/job/${element.id}`])
  }
}
