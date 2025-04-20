import { CommonModule } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatOption, provideNativeDateAdapter } from '@angular/material/core';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import {MatTimepickerModule} from '@angular/material/timepicker';
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface';
import { AddSelectDialogComponentComponent } from '../add-select-dialog-component/add-select-dialog-component.component';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';

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
  minTime: Date
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
      startTime: ['', Validators.required],
      endTime: ['', Validators.required],
      bookingType: ['', Validators.required],
      jobID: ['', Validators.required],
      jobDescription: [''],
      status: ['', Validators.required],
      color: ['']
    })

    this.typeOfDialog = this.data.typeOfDialog
    this.minTime = new Date(this.data.startTime)
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
        startTime: new Date(this.data.startTime),
        endTime: new Date(this.data.endTime),
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

  openAddJobDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'job',
      dialogData: this.jobID,
      searchHint: 'Search by job description',
      headers: ['Description','Job Status', 'Start Date', 'End Date', 'Customer Name'],
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
        startTime: this.eventForm.get('startTime')?.value,
        endTime: this.eventForm.get('endTime')?.value,
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
