import { CommonModule } from '@angular/common';
import { Component, Inject } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatOption } from '@angular/material/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-booking-event-dialog-component',
  imports: [
    MatDialogModule,
    MatButtonModule,
    MatInputModule,
    ReactiveFormsModule,
    FormsModule,
    MatOption,
    MatSelectModule,
    CommonModule
  ],
  templateUrl: './booking-event-dialog-component.component.html',
  styleUrl: './booking-event-dialog-component.component.scss'
})

export class BookingEventDialogComponentComponent {
  selectedTime!: string;
  timeOptions: string[];

  constructor(
    public dialogRef: MatDialogRef<BookingEventDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { start: string }
  ) {
    this.timeOptions = this.generateEndTimes(data.start);
  }

  private generateEndTimes(start: string): string[] {
    const [startHour, startMinute] = start.split(':').map(Number);
    const options: string[] = [];
    for (let h = startHour; h <= 19; h++) {
      if (h === startHour && startMinute < 30) {
        options.push(`${h}:${startMinute + 30}`);
      }
      if (h > startHour) {
        options.push(`${h}:00`);
        options.push(`${h}:30`);
      }
    }
    return options;
  }

  save(): void {
    this.dialogRef.close(this.selectedTime);
  }
}
