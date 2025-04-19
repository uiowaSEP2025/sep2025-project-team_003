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
import { JobDataInterface } from '../../interfaces/api-responses/job.api.data.interface';
import { JobService } from '../../services/job.service';
import { Router } from '@angular/router';

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
  jobData: JobDataInterface | null = null;

  constructor (
    public dialogRef: MatDialogRef<ViewJobDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any ) 
  {
    this.jobData = this.data[0]
  }

  ngOnInit() {
    
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }
}
