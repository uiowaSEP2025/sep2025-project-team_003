import {Component, Input, OnInit} from '@angular/core';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { JobService } from '../../../services/job.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import {Job} from '../../../interfaces/job.interface';

@Component({
  selector: 'app-view-job-page',
  imports: [
    LoadingFallbackComponent,
    CommonModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatListModule,
    MatDividerModule,
    MatExpansionModule,
  ],
  templateUrl: './view-job-page.component.html',
  styleUrl: './view-job-page.component.scss'
})
export class ViewJobPageComponent  implements OnInit {
  loading = false;
  jobID!: number
  @Input() jobData: Job = {
    customer: {
      customerID: 0,
      organizationID: 0,
      notes: '',
      firstName: '',
      lastName: '',
      email: '',
      phone: ''
    },
    description: '',
    endDate: new Date(),
    id: 0,
    jobAddress: '',
    jobCity: '',
    jobState: '',
    jobStatus: 'created',
    jobZip: '',
    materials: [],
    services: [],
    startDate: new Date()

  }

  constructor (private jobService: JobService, private activatedRoute:ActivatedRoute, private router: Router, private errorHandler: ErrorHandlerService) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.jobID = Number(params.get('id'));
    })
  }

  ngOnInit(): void {
    this.loading = true;
    this.jobService.getSpecificJobData(this.jobID).subscribe(
      {next: (response) => {
        this.jobData = response;
        this.loading = false;
      },
      error: (error) => {
        this.errorHandler.handleError(error);
        this.loading = false;
      }}
    )
  }

  navigateToPage(pagePath: string) {
    void this.router.navigate([`/${pagePath}`]);
  }
}
