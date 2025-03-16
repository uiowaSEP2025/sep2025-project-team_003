import { Component, ChangeDetectionStrategy, Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatError } from '@angular/material/form-field';
import { CommonModule } from '@angular/common';



@Component({
  imports: [MatCardModule, MatFormFieldModule, MatDatepickerModule, MatInputModule, MatError, CommonModule],
  selector: 'app-invoice-date-picker',
  templateUrl: './invoice-date-picker.component.html',
  providers: [provideNativeDateAdapter()],
  styleUrl: './invoice-date-picker.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class InvoiceDatePickerComponent {
  @Input({ required: true }) formControll!: any // extra l to avoid name conflict
  isInvalidRange = false

  validate():boolean {
    return true
  }

}
