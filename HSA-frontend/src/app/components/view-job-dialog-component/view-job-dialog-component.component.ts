import { CommonModule } from '@angular/common';
import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { JobDisplayTableComponent } from '../job-display-table/job-display-table.component';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { JobDataInterface } from '../../interfaces/api-responses/job.api.data.interface';

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
  standalone: true,
  styleUrl: './view-job-dialog-component.component.scss'
})
export class ViewJobDialogComponentComponent  {
  jobData: JobDataInterface | null = null;
  bookingData: any;

  constructor (
    public dialogRef: MatDialogRef<ViewJobDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any

  )
  {
    this.jobData = this.data.jobInfo
    this.bookingData = this.data.bookingInfo
  }



  onCancel(): void {
    this.dialogRef.close(false);
  }
}
