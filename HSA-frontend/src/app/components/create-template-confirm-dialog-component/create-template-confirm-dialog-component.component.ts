import { Component, Inject, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { JobDisplayTableComponent } from '../job-display-table/job-display-table.component';
import { JobTemplateDataInterface } from '../../interfaces/api-responses/jobTemplate.api.data.interface';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-template-confirm-dialog-component',
  imports: [
    MatDialogModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    JobDisplayTableComponent,
    ReactiveFormsModule,
    LoadingFallbackComponent
  ],
  templateUrl: './create-template-confirm-dialog-component.component.html',
  styleUrl: './create-template-confirm-dialog-component.component.scss'
})
export class CreateTemplateConfirmDialogComponentComponent {
  jobTemplateData: JobTemplateDataInterface | null = null;
  jobTemplateForm: FormGroup;
  currentDescription: string = ""

  constructor(
    public dialogRef: MatDialogRef<CreateTemplateConfirmDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private jobTemplateFormBuilder: FormBuilder,
    private snackBar: MatSnackBar,
  ) {
    this.jobTemplateData = data
    this.jobTemplateForm = this.jobTemplateFormBuilder.group({
      description: [data.description, Validators.required],
      name: ['', Validators.required]
    })
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onConfirm(): void {
    if (this.jobTemplateForm.invalid) {
      this.jobTemplateForm.markAllAsTouched();
      this.snackBar.open('Invalid fields, please revise the form and resubmit', '', {
        duration: 3000
      });
    }

    this.dialogRef.close({
      description: this.jobTemplateForm.get('description')?.value,
      name: this.jobTemplateForm.get('name')?.value,
      services: this.jobTemplateData?.services,
      materials: this.jobTemplateData?.materials
    });
  }
}
