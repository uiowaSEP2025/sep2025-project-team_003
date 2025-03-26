import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-update-confirm-dialog-component',
  imports: [
    MatDialogModule,
    MatButtonModule
  ],
  templateUrl: './update-confirm-dialog-component.component.html',
  styleUrl: './update-confirm-dialog-component.component.scss'
})
export class UpdateConfirmDialogComponentComponent {
  itemDescription: any
    constructor(
      public dialogRef: MatDialogRef<UpdateConfirmDialogComponentComponent>,
      @Inject(MAT_DIALOG_DATA) public message: any,
    ) {
      this.itemDescription = message;
    }
  
    onCancel(): void {
      this.dialogRef.close(false);
    }
  
    onConfirm(): void {
      this.dialogRef.close(true);
    }
}
