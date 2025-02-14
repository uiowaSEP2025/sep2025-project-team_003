import { Component } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { FormControl,ReactiveFormsModule,Validators } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import {MatButtonModule} from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { ViewChild } from '@angular/core';

@Component({
  selector: 'app-create-customer-page',
  imports: [FormsModule, MatInputModule, ReactiveFormsModule, MatButtonModule, MatIconModule],
  templateUrl: './create-customer-page.component.html',
  styleUrl: './create-customer-page.component.scss'
})
export class CreateCustomerPageComponent {
  firstNameControl = new FormControl('', Validators.required)
  lastNameControl = new FormControl('', Validators.required)
  emailControl = new FormControl('', [Validators.email, Validators.required])
  phoneControl = new FormControl('', Validators.required)
  notesControl = new FormControl('')
  matcher = new GenericFormErrorStateMatcher()
}
