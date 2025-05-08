import { Component, inject, model} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {
  MatDialogActions,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'invoice-state-regression-confirmer',
  templateUrl: 'invoice-state-regression-confirmer.component.html',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
  ],
})
export class InvoiceStateRegressionConfirmerComponent {
  readonly dialogRef = inject(MatDialogRef<InvoiceStateRegressionConfirmerComponent>);
  readonly status = inject<'created' | 'issued' | 'paid' >(MAT_DIALOG_DATA);


  onNoClick(): void {
    this.dialogRef.close(false);
  }

  onConfirm():void {
    this.dialogRef.close(true)
  }
}