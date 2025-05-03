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
import { AddSelectDialogComponentComponent } from '../add-select-dialog-component/add-select-dialog-component.component';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { generateTimes } from '../../utils/generate-time-utils';
import { StringFormatter } from '../../utils/string-formatter';
import parseTimeToDate from '../../utils/date-parse-from-HHMM';


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
  selectedJob: any
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
    private stringFormatter: StringFormatter
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
    this.colors = this.data.listOfColor
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
        color: this.data.backColor
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
      console.log(startTime, endTime)

      const start = parseTimeToDate(startTime)
      const end = parseTimeToDate(endTime)
      if (start >= end) {
        const endIdx = this.startTimes.indexOf(endTime)
        this.eventForm.get('startTime')?.setValue(this.startTimes[endIdx - 1])
      }
    });

    
  }


  openAddJobDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'job',
      dialogData: this.jobID,
      searchHint: 'Search by job description',
      headers: ['Description', 'Job Status', 'Start Date', 'End Date', 'Customer Name'],
      materialInputFields: [],
    };

    const dialogRef = this.dialog.open(AddSelectDialogComponentComponent, {
      width: 'auto',
      maxWidth: '90vw',
      height: 'auto',
      maxHeight: '90vh',
      data: dialogData
    });

    dialogRef.afterClosed().subscribe((result: any) => {
      if (result.length !== 0) {
        let jobEntry = result.itemsInfo[0]
        this.eventForm.controls['jobID'].setValue(jobEntry.id)
        this.eventForm.controls['jobDescription'].setValue(jobEntry.description)
        this.jobID = jobEntry.id;
        this.selectedJob = jobEntry
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
