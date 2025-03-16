import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
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

@Component({
  imports: [MatCardModule, MatFormFieldModule, MatDatepickerModule, MatInputModule, MatError, CommonModule, ReactiveFormsModule],
  selector: 'app-invoice-date-picker',
  templateUrl: './invoice-date-picker.component.html',
  providers: [provideNativeDateAdapter()],
  styleUrl: './invoice-date-picker.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class InvoiceDatePickerComponent {
  @Input({ required: true }) formControll!: FormGroup<DateRange> // extra l to avoid name conflict
  isInvalidRange = false

  validate():boolean {
    console.log(this.formControll.controls.start.value)
    return true
  }

}
