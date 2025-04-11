import {Component, Input, OnInit} from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import {Job, JobTable} from '../../../interfaces/job.interface';
import { JobsHelperComponent} from '../jobs-helper/jobs-helper.component';
import {JobService} from '../../../services/job.service';


@Component({
  selector: 'app-edit-job-page',
  providers: [
    provideNativeDateAdapter()
  ],
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatListModule,
    MatDividerModule,
    MatExpansionModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatSelectModule,
    MatDatepickerModule,
    JobsHelperComponent
  ],
  templateUrl: './edit-job-page.component.html',
  styleUrl: './edit-job-page.component.scss'
})
export class EditJobPageComponent implements OnInit {
  @Input() jobSimple: JobTable = {
    customerName: '',
    description: '',
    endDate: new Date(),
    id: 0,
    jobStatus: 'created',
    startDate: new Date()
  }
  job: Job = {
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
    startDate: new Date(),

  };
  constructor(private jobService: JobService) {
  }

  ngOnInit() {
    this.jobService.getSpecificJobData(this.jobSimple.id).subscribe(response => {
      this.job = response;
    }
    )
  }
}
