import { Component, Inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-add-confirm-dialog-component',
  imports: [
    MatDialogModule,
    MatButtonModule
  ],
  templateUrl: './add-confirm-dialog-component.component.html',
  styleUrl: './add-confirm-dialog-component.component.scss'
})
export class AddConfirmDialogComponentComponent {
  itemDescription: any
    
  constructor(
    public dialogRef: MatDialogRef<AddConfirmDialogComponentComponent>,
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
