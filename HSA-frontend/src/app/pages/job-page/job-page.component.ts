import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { JobService } from '../../services/job.service';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';

@Component({
  selector: 'app-job-page',
  imports: [TableComponentComponent, MatButtonModule, MatIconModule, LoadingFallbackComponent],
  templateUrl: './job-page.component.html',
  styleUrl: './job-page.component.scss'
})
export class JobPageComponent implements OnInit  {
  jobs: any
  jobService: JobService

  constructor(private router: Router, jobService: JobService) {
    this.jobService = jobService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.jobService.getJob({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.jobs = response
      },
      error: (error) => {
          if (error.status === 401) {
            this.router.navigate(['/login']);
          }
      }
    })
  }

  redirectJobDetails(element: any) {
    this.router.navigate([`/job/${element.id}`])
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
