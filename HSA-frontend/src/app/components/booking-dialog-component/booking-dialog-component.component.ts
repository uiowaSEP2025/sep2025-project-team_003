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
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BookingJobsPerContractorComponent } from '../booking-jobs-per-contractor/booking-jobs-per-contractor.component';

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
    provideNativeDateAdapter()
  ],
  templateUrl: './booking-dialog-component.component.html',
  styleUrl: './booking-dialog-component.component.scss'
})
export class BookingDialogComponentComponent implements OnInit {
  eventForm: FormGroup;
  jobID: number = 0
  selectedJob: any
  colors: any
  currentColor: any
  typeOfDialog: string

  constructor(
    public dialog: MatDialog,
    public dialogRef: MatDialogRef<BookingDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private eventFormBuilder: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    this.eventForm = this.eventFormBuilder.group({
      eventName: ['', Validators.required],
      bookingType: ['', Validators.required],
      jobID: ['', Validators.required],
      jobDescription: [''],
      status: ['', Validators.required],
      color: ['']
    })

    this.typeOfDialog = this.data.typeOfDialog
    this.colors = this.data.listOfColor
  }

  ngOnInit() {
    if (this.typeOfDialog === "create") {
      this.eventForm.patchValue({
        startTime: new Date(this.data.startTime),
        status: "pending"
      })
    } else {
      this.eventForm.setValue({
        eventName: this.data.eventName,
        bookingType: this.data.bookingType,
        jobID: this.data.jobID,
        status: this.data.status,
        jobDescription: this.data.jobDescription,
        color: this.data.backColor
      });

      this.currentColor = this.data.backColor
      this.eventForm.markAllAsTouched();
    }
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
      height: 'auto',
      data: { contractorId: this.data.contractorId }
    });

    dialogRef.afterClosed().subscribe((result: any) => {
      // if (result.length !== 0) {
      //   let jobEntry = result.itemsInfo[0]
      //   this.eventForm.controls['jobID'].setValue(jobEntry.id)
      //   this.eventForm.controls['jobDescription'].setValue(jobEntry.description)
      //   this.jobID = jobEntry.id;
      //   this.selectedJob = jobEntry
      // }
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
    } else {
      this.dialogRef.close({
        eventName: this.eventForm.get('eventName')?.value,
        startTime: this.data.startTime,
        endTime: this.data.endTime,
        backColor: this.getColorID(),
        tags: {
          jobID: this.eventForm.get('jobID')?.value,
          jobDescription: this.eventForm.get('jobDescription')?.value,
          bookingType: this.eventForm.get('bookingType')?.value,
          status: this.eventForm.get('status')?.value,
        }
      });
    }
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
