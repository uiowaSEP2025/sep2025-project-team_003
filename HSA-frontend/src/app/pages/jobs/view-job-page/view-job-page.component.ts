import { Component, OnInit } from '@angular/core';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { JobDisplayTableComponent } from '../../../components/job-display-table/job-display-table.component';
import { JobService } from '../../../services/job.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { JobDataInterface } from '../../../interfaces/api-responses/job.api.data.interface';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-view-job-page',
  imports: [
    LoadingFallbackComponent,
    CommonModule,
    MatButtonModule,
    MatIconModule,
    JobDisplayTableComponent,
    MatCardModule,
    MatListModule,
    MatDividerModule,
    MatExpansionModule,
  ],
  templateUrl: './view-job-page.component.html',
  styleUrl: './view-job-page.component.scss'
})
export class ViewJobPageComponent  implements OnInit {
  jobID!: number
  jobData: JobDataInterface | null = null;

  constructor (private jobService: JobService, private activatedRoute:ActivatedRoute, private router: Router, private errorHandler: ErrorHandlerService) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.jobID = Number(params.get('id'));
    })
  }

  ngOnInit(): void {
    this.jobService.getSpecificJobData(this.jobID).subscribe(
      {next: (response) => {
        this.jobData = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }}
    )
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
