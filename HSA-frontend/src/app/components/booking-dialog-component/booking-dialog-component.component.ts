import { CommonModule } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatOption, provideNativeDateAdapter } from '@angular/material/core';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTimepickerModule } from '@angular/material/timepicker';
import { generateTimes } from '../../utils/generate-time-utils';
import { StringFormatter } from '../../utils/string-formatter';
import parseTimeToDate from '../../utils/date-parse-from-HHMM';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BookingJobsPerContractorComponent } from '../booking-jobs-per-contractor/booking-jobs-per-contractor.component';
import { BookingService } from '../../services/calendar-data.service';


@Component({
  selector: 'app-booking-dialog-component',
  imports: [
    CommonModule,
    MatCardModule,
    MatDialogModule,
    MatSelectModule,
    MatOption,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    MatTimepickerModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [
    provideNativeDateAdapter(),
  ],
  templateUrl: './booking-dialog-component.component.html',
  styleUrl: './booking-dialog-component.component.scss'
})
export class BookingDialogComponentComponent implements OnInit {
  eventForm: FormGroup;
  jobID: number = 0
  colors: any
  currentColor: any
  typeOfDialog: string
  startTimes!: String[]
  endTimes!: String[]


  constructor(
    public dialog: MatDialog,
    public dialogRef: MatDialogRef<BookingDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private eventFormBuilder: FormBuilder,
    private snackBar: MatSnackBar,
    private stringFormatter: StringFormatter,
    private colorService: BookingService
  ) {
    this.eventForm = this.eventFormBuilder.group({
      eventName: ['', Validators.required],
      bookingType: ['', Validators.required],
      jobID: ['', Validators.required],
      jobDescription: [''],
      status: ['', Validators.required],
      color: [''],
      startTime: [null],
      endTime: [null]
    })


    this.typeOfDialog = this.data.typeOfDialog
    this.colors = this.colorService.getColors()

  }

  private selectionToDate(timeString: String): Date {
    const originalDate = new Date(this.data.startTime);

    const [time, period] = timeString.split(' ');
    const [hours, minutes] = time.split(':').map(num => parseInt(num, 10));

    let hours24 = hours;
    if (period === 'PM' && hours !== 12) {
      hours24 += 12;
    } else if (period === 'AM' && hours === 12) {
      hours24 = 0;
    }

    originalDate.setHours(hours24, minutes, 0, 0);
    return originalDate;
  }
  ngOnInit() {
    this.startTimes = generateTimes(false, this.data.startTime).map(date => this.stringFormatter.formatDateToHHMM(date));
    this.endTimes = generateTimes(true, this.data.endTime).map(date => this.stringFormatter.formatDateToHHMM(date));

    if (this.typeOfDialog === "create") {
      this.eventForm.patchValue({
        startTime: this.stringFormatter.formatDateToHHMM(new Date(this.data.startTime)),
        endTime: this.stringFormatter.formatDateToHHMM(new Date(this.data.endTime)),
        status: "pending"
      })
    } else {
      this.eventForm.setValue({
        eventName: this.data.eventName,
        bookingType: this.data.bookingType,
        jobID: this.data.jobID,
        status: this.data.status,
        jobDescription: this.data.jobDescription,
        color: this.data.backColor,
        startTime: this.stringFormatter.formatDateToHHMM(new Date(this.data.startTime)),
        endTime: this.stringFormatter.formatDateToHHMM(new Date(this.data.endTime)),
      });

      this.currentColor = this.data.backColor
      this.eventForm.markAllAsTouched();
    }

    this.eventForm.get('startTime')?.valueChanges.subscribe((startTime: string) => {
      const endTime = this.eventForm.get('endTime')?.value;
      const start = parseTimeToDate(startTime)
      const end = parseTimeToDate(endTime)
      if (start >= end) {
        const startIdx = this.endTimes.indexOf(startTime)
        this.eventForm.get('endTime')?.setValue(this.endTimes[startIdx + 1])
      }
    });

    this.eventForm.get('endTime')?.valueChanges.subscribe((endTime: string) => {
      const startTime = this.eventForm.get('startTime')?.value;

      const start = parseTimeToDate(startTime)
      const end = parseTimeToDate(endTime)
      if (start >= end) {
        const endIdx = this.startTimes.indexOf(endTime)
        this.eventForm.get('startTime')?.setValue(this.startTimes[endIdx - 1])
      }
    });


  }



  formatTime(input: string): string {
    const date = new Date(input);
    let hours = date.getHours();
    const minutes = date.getMinutes();

    const ampm = hours >= 12 ? ' PM' : ' AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'

    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;

    return `${hours}:${formattedMinutes}${ampm}`;
  }

  openAddJobDialog() {

    const dialogRef = this.dialog.open(BookingJobsPerContractorComponent, {
      width: 'auto',
      maxWidth: '90vw',
      height: 'auto',
      maxHeight: '90vh',
      data: { contractorId: this.data.contractorId }
    });

    dialogRef.afterClosed().subscribe((result: { id: number, desc: string }) => {
      if (result) {
        this.jobID = result.id
        this.eventForm.get('jobID')?.setValue(result.id)
        this.eventForm.get('jobID')!.markAsUntouched()
        this.eventForm.get('jobDescription')!.setValue(result.desc)
      }
    })
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onSubmit() {
    if (this.eventForm.invalid) {
      this.eventForm.markAllAsTouched()
      this.snackBar.open('Invalid fields. Please review the form and submit again!', '', {
        duration: 3000
      });
    }
    this.dialogRef.close({
      eventName: this.eventForm.get('eventName')?.value,
      startTime: this.selectionToDate(this.eventForm.get('startTime')!.value),
      endTime: this.selectionToDate(this.eventForm.get('endTime')!.value),
      backColor: this.getColorID(),
      tags: {
        jobID: this.eventForm.get('jobID')?.value,
        jobDescription: this.eventForm.get('jobDescription')?.value,
        bookingType: this.eventForm.get('bookingType')?.value,
        status: this.eventForm.get('status')?.value,
      }
    });

  }

  getColorID() {
    let chosenColor: any
    this.colors.forEach((element: any) => {
      if (element.id === this.eventForm.get('color')?.value) {
        chosenColor = element.id
      }
    });

    return chosenColor
  }

  getColorNameViaID(id: string) {
    let chosenColor: any
    this.colors.forEach((element: any) => {
      if (element.id === id) {
        chosenColor = element
      }
    });

    return chosenColor
  }
}
