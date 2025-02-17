import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatFormFieldModule, } from '@angular/material/form-field';
import { ReactiveFormsModule, FormControl, Validators, FormsModule } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-edit-customer-page',
  imports: [MatFormFieldModule, ReactiveFormsModule, MatInputModule, MatButtonModule, FormsModule],
  templateUrl: './edit-customer-page.component.html',
  styleUrl: './edit-customer-page.component.scss'
})
export class EditCustomerPageComponent implements OnInit {
  email!: string
  firstName!: string
  lastName!: string
  phoneNo!: string

  constructor(private activatedRoute: ActivatedRoute) { }
  firstNameControl = new FormControl('', Validators.required)
  lastNameControl = new FormControl('', Validators.required)
  emailControl = new FormControl('', [Validators.email, Validators.required])
  phoneControl = new FormControl('', Validators.required)
  notesControl = new FormControl('')
  matcher = new GenericFormErrorStateMatcher()


  ngOnInit() {
    // pass existing field in as a query param
    this.activatedRoute.queryParams.subscribe(params => {
      this.email = params['email'];
      this.firstName = params['fname'];
      this.lastName = params['lname'];
      this.phoneNo = params['phoneno'];
      this.firstNameControl.setValue(this.firstName);
      this.lastNameControl.setValue(this.lastName);
      this.emailControl.setValue(this.email);
      this.phoneControl.setValue(this.phoneNo);
    });
  }

}
