import { Component } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import {CustomersHelperComponent} from '../customers-helper/customers-helper.component';

@Component({
  selector: 'app-create-customer-page',
  imports: [FormsModule, MatInputModule, ReactiveFormsModule, MatButtonModule, MatIconModule, CustomersHelperComponent],
  templateUrl: './create-customer-page.component.html',
  styleUrl: './create-customer-page.component.scss'
})
export class CreateCustomerPageComponent {

}
