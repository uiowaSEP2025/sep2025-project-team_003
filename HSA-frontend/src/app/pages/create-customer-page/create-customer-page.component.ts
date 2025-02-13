import { Component } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { PhoneNumberInputComponent } from '../../components/phone-number-input/phone-number-input-component';
import { FormControl } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';

@Component({
  selector: 'app-create-customer-page',
  imports: [MatInputModule,PhoneNumberInputComponent, ReactiveFormsModule],
  templateUrl: './create-customer-page.component.html',
  styleUrl: './create-customer-page.component.scss'
})
export class CreateCustomerPageComponent {
  firstNameControl = new FormControl('')
  matcher = new GenericFormErrorStateMatcher()
}
