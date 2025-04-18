import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTableModule } from '@angular/material/table';
import { BookingEventDialogComponentComponent } from '../../components/booking-event-dialog-component/booking-event-dialog-component.component';

@Component({
  selector: 'app-booking-page',
  imports: [
    FormsModule, 
    MatFormFieldModule, 
    MatInputModule, 
    MatButtonModule,
    MatCardModule,
    ReactiveFormsModule,
    CommonModule,
    MatTableModule,
    MatCardModule
  ],
  templateUrl: './booking-page.component.html',
  styleUrl: './booking-page.component.scss'
})
export class BookingPageComponent {
  resources = ['Room A', 'Room B', 'Room C', 'Room D'];
  interval = 30; // minutes
  timeSlots: string[] = [];

  events: { resource: string, start: string, end: string }[] = [];

  constructor(private dialog: MatDialog) {}

  ngOnInit(): void {
    this.generateTimeSlots();
  }

  toggleInterval(): void {
    this.interval = this.interval === 60 ? 30 : 60;
    this.generateTimeSlots();
  }

  generateTimeSlots(): void {
    const slots: string[] = [];
    const startHour = 8;
    const endHour = 20;

    for (let h = startHour; h < endHour; h++) {
      slots.push(`${h}:00`);
      if (this.interval === 30) {
        slots.push(`${h}:30`);
      }
    }

    this.timeSlots = slots;
  }

  async openDialog(resource: string, startTime: string): Promise<void> {
    const dialogRef = this.dialog.open(BookingEventDialogComponentComponent, {
      data: { start: startTime }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.events.push({ resource, start: startTime, end: result });
      }
    });
  }

  isSlotInEvent(resource: string, time: string): boolean {
    const slotMinutes = this.toMinutes(time);
    return this.events.some(event => {
      if (event.resource !== resource) return false;
      const start = this.toMinutes(event.start);
      const end = this.toMinutes(event.end);
      return slotMinutes >= start && slotMinutes < end;
    });
  }

  private toMinutes(time: string): number {
    const [h, m] = time.split(':').map(Number);
    return h * 60 + (m || 0);
  }
}
