import { Component, Inject, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { JobTemplateService } from '../../services/jobTemplate.service';
import { ErrorHandlerService } from '../../services/error.handler.service';
import { JobDisplayTableComponent } from "../job-display-table/job-display-table.component";
import { JobTemplateDataInterface } from '../../interfaces/api-responses/jobTemplate.api.data.interface';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';

@Component({
  selector: 'app-apply-template-confirm-dialog-component',
  imports: [
    MatDialogModule,
    MatButtonModule,
    JobDisplayTableComponent,
    LoadingFallbackComponent
],
  templateUrl: './apply-template-confirm-dialog-component.component.html',
  styleUrl: './apply-template-confirm-dialog-component.component.scss'
})
export class ApplyTemplateConfirmDialogComponentComponent implements OnInit {
  templateID: any
  jobTemplateData: JobTemplateDataInterface | null = null;
    
  constructor(
    public dialogRef: MatDialogRef<ApplyTemplateConfirmDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private jobTemplateService: JobTemplateService,
    private errorHandler: ErrorHandlerService,
  ) {
    this.templateID = data;
  }

  ngOnInit(): void {
    this.jobTemplateService.getSpecificJobTemplateData(this.templateID).subscribe({
      next: (response) => {
        this.jobTemplateData = response
      },
      error: (error) => {
        this.errorHandler.handleError(error);
      }
    })
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onConfirm(): void {
    this.dialogRef.close({
      jobDescription: this.jobTemplateData?.data.description,
      services: this.jobTemplateData?.services,
      materials: this.jobTemplateData?.materials
    });
  }
}
