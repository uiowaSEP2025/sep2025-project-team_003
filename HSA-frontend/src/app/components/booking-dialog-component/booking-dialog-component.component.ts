import { CommonModule } from '@angular/common';
import { Component, Inject } from '@angular/core';
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
export class BookingDialogComponentComponent {
  eventForm: FormGroup;
  jobID: number = 0
  selectedJob: number = 0
  minTime: Date
  colors: any

  constructor(
    public dialog: MatDialog,
    public dialogRef: MatDialogRef<BookingDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private eventFormBuilder: FormBuilder,
  ) {
    this.eventForm = this.eventFormBuilder.group({
      eventName: ['', Validators.required],
      startTime: ['', Validators.required],
      endTime: ['', Validators.required],
      bookingType: ['', Validators.required],
      jobID: ['', Validators.required],
      jobDescription: [''],
      color: ['']
    })

    this.eventForm.patchValue({
      startTime: new Date(this.data.startTime)
    })

    this.minTime = new Date(this.data.startTime)
    this.colors = this.data.listOfColor
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
        this.selectedJob = jobEntry.id
      }
    })
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onSubmit() {
    if (this.eventForm.invalid) {
      this.eventForm.markAllAsTouched()
    } else {
      this.dialogRef.close({
        eventName: this.eventForm.get('eventName')?.value,
        startTime: this.eventForm.get('startTime')?.value,
        endTime: this.eventForm.get('endTime')?.value,
        bookingType: this.eventForm.get('bookingType')?.value,
        color: this.getColor()
      });
    }
  }

  getColor() {
    let chosenColor: any
    this.colors.forEach((element: any) => {
      if (element.id === this.eventForm.get('color')?.value) {
        chosenColor = element
      }
    });

    return chosenColor
  }
}
