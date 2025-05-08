import { Component, Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatError } from '@angular/material/form-field';
import { CommonModule } from '@angular/common';
import { DateRange } from '../../pages/edit-invoice-page/edit-invoice-page.component';
import { FormGroup } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

@Component({
  imports: [MatCardModule, MatFormFieldModule, MatDatepickerModule, MatInputModule, MatError, CommonModule, ReactiveFormsModule],
  selector: 'app-invoice-date-picker',
  templateUrl: './invoice-date-picker.component.html',
  providers: [provideNativeDateAdapter()],
  styleUrl: './invoice-date-picker.component.scss',
})
export class InvoiceDatePickerComponent implements OnInit{
  @Input({ required: true }) formControll!: FormGroup<DateRange> // extra l to avoid name conflict
  @Input() dateLabels: string[] = ["Start Date", "End Date"]
  isInvalidRange = false
  isNullError = false
  private valueChangesSub!: Subscription;


  ngOnInit(): void {
    this.valueChangesSub = this.formControll.valueChanges.subscribe(value => {
      if (value.issued !== null && value.due !== null) {
        this.validate()
      }
    });}

  validate(): boolean {
    // only call this when visable
    this.isInvalidRange = false
    this.isNullError = false
    const issued = this.formControll.controls.issued.value;
    const due = this.formControll.controls.due.value;
    if (!issued || !due) {
      this.isNullError = true
      return false
    }

    if (issued > due) {
      this.isInvalidRange = true;
      return false;
    }

    this.isInvalidRange = false;
    return true;
  }

  ngOnDestroy(): void {
    this.valueChangesSub.unsubscribe();
  }

}
