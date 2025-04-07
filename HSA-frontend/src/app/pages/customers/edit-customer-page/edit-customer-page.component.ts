import {Component, Input} from '@angular/core';
import { MatFormFieldModule, } from '@angular/material/form-field';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { CustomersHelperComponent} from '../customers-helper/customers-helper.component';
import {Customer} from '../../../interfaces/customer.interface';

@Component({
  selector: 'app-edit-customer-page',
  imports: [
    MatFormFieldModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    FormsModule,
    CustomersHelperComponent
  ],
  templateUrl: './edit-customer-page.component.html',
  styleUrl: './edit-customer-page.component.scss'
})
export class EditCustomerPageComponent {

  @Input() customer: Customer = {
    organizationID: 0,
    customerID: 0,
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    notes: ''
  };

}
