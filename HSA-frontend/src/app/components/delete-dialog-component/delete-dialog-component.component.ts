import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { StringFormatter } from '../../utils/string-formatter';

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
  itemDescription: any
  
  constructor(
    public dialogRef: MatDialogRef<DeleteDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    stringFormatter: StringFormatter
  ) {
    this.itemDescription = stringFormatter.formatJSONData(data)
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onConfirm(): void {
    this.dialogRef.close(true);
  }
}
