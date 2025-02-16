import { Component } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule,FormControl,ReactiveFormsModule,Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';

@Component({
  selector: 'app-edit-contractors-page',
  imports: [MatFormFieldModule, ReactiveFormsModule, MatInputModule, MatButtonModule, FormsModule],
  templateUrl: './edit-contractors-page.component.html',
  styleUrl: './edit-contractors-page.component.scss'
})
export class EditContractorsPageComponent {
  email!: string
  firstName!: string
  lastName!: string
  phoneNo!: string

  constructor(private activatedRoute: ActivatedRoute) { }
    firstNameControl = new FormControl('', Validators.required)
    lastNameControl = new FormControl('', Validators.required)
    emailControl = new FormControl('', [Validators.email, Validators.required])
    phoneControl = new FormControl('', Validators.required)
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

}}
