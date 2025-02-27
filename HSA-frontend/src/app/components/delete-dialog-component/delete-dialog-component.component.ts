import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-delete-dialog-component',
  imports: [
    MatDialogModule,
    MatButtonModule
  ],
  templateUrl: './delete-dialog-component.component.html',
  styleUrl: './delete-dialog-component.component.scss'
})
export class DeleteDialogComponentComponent {
  constructor(
    public dialogRef: MatDialogRef<DeleteDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onConfirm(): void {
    this.dialogRef.close(true);
  }
}
