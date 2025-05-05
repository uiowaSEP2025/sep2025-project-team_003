import { CommonModule } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { JobDisplayTableComponent } from '../job-display-table/job-display-table.component';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { ContractorJSON, JobDisplayInterface, MaterialJSON, ServiceJSON } from '../../interfaces/api-responses/job.api.display.interface';



interface JobData {
  id: number;
  jobStatus: string;
  startDate: string;
  endDate: string;
  description: string;
  customerName: string;
  customerID: number;
  requestorAddress: string;
  requestorCity: string;
  requestorState: string;
  requestorZip: string;
}

interface JobDetails {
  data: JobData;
  services: ServiceJSON[];  
  materials: MaterialJSON[];
  contractors: ContractorJSON[];
}

@Component({
  selector: 'app-view-job-dialog-component',
  imports: [
    CommonModule,
    MatDialogModule,
    LoadingFallbackComponent, 
    MatButtonModule,
    MatIconModule, 
    JobDisplayTableComponent, 
    MatCardModule,
    MatListModule,
    MatDividerModule,
    MatExpansionModule
  ],
  templateUrl: './view-job-dialog-component.component.html',
  styleUrl: './view-job-dialog-component.component.scss'
})
export class ViewJobDialogComponentComponent implements OnInit {
  jobData: JobDetails | null = null;
  servicesMaterialsContractors!: JobDisplayInterface;
  bookingData: any;



  constructor (
    public dialogRef: MatDialogRef<ViewJobDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any ) 
  {
    this.jobData = this.data.jobInfo
    this.bookingData = this.data.bookingInfo
    this.servicesMaterialsContractors =  {
        'services': [],
        'materials': [],
        'contractors': this.jobData?.contractors!,
    }
  }

  ngOnInit() {
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }
}
