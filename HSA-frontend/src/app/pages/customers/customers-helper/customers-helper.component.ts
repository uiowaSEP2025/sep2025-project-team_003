import {Component, Input, OnInit} from '@angular/core';
import {FormControl, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from '@angular/material/dialog';
import {MatInput, MatLabel} from '@angular/material/input';
import {MatError, MatFormField} from '@angular/material/form-field';
import {MatButton} from '@angular/material/button';
import {GenericFormErrorStateMatcher} from '../../../utils/generic-form-error-state-matcher';
import {CreateCustomerPageComponent} from '../create-customer-page/create-customer-page.component';
import {CustomerService} from '../../../services/customer.service';
import {ActivatedRoute, Router} from '@angular/router';
import {ErrorHandlerService} from '../../../services/error.handler.service';
import {Customer} from '../../../interfaces/customer.interface';
import {phoneValidator} from '../../../utils/phone-validator';

@Component({
  selector: 'app-customers-helper',
  imports: [
    FormsModule,
    MatButton,
    MatDialogActions,
    MatDialogClose,
    MatDialogContent,
    MatError,
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule,
    MatDialogTitle
  ],
  templateUrl: './customers-helper.component.html',
  styleUrl: './customers-helper.component.scss'
})
export class CustomersHelperComponent implements OnInit {
  @Input() crudType: 'Create' | 'Update' = 'Create';
  firstNameControl = new FormControl('', Validators.required)
  lastNameControl = new FormControl('', Validators.required)
  emailControl = new FormControl('', [Validators.email, Validators.required])
  phoneControl = new FormControl('', Validators.required, phoneValidator())
  notesControl = new FormControl('')
  matcher = new GenericFormErrorStateMatcher()

  private isFormValid() {
    return this.firstNameControl.valid &&
      this.lastNameControl.valid &&
      this.emailControl.valid &&
      this.phoneControl.valid;
  }

  constructor(private activatedRoute: ActivatedRoute, public dialogRef: MatDialogRef<CreateCustomerPageComponent>, private customerService: CustomerService, private router: Router, private errorHandler: ErrorHandlerService) {
  }

  email!: string
  @Input() customer!: Customer;

  ngOnInit() {
    if (this.crudType === 'Update') {
      this.firstNameControl = new FormControl(this.customer.firstName, Validators.required)
      this.lastNameControl = new FormControl(this.customer.lastName, Validators.required)
      this.emailControl = new FormControl(this.customer.email, [Validators.email, Validators.required])
      this.phoneControl = new FormControl(this.customer.phone, Validators.required, phoneValidator())
      this.notesControl = new FormControl(this.customer.notes)
    }
  }

  onSubmit() {
    if (!this.isFormValid()) {
      return
    }

    if (this.crudType === 'Update') {
      const args = {
        id: this.customer.customerID,
        first_name: this.firstNameControl.value,
        last_name: this.lastNameControl.value,
        email: this.emailControl.value,
        phone: this.phoneControl.value,
        notes: this.notesControl.value
      }
      this.customerService.editCustomer(args).subscribe(
        {
          next: () => {
            this.dialogRef.close();
            window.location.reload();
          },
          error: (error) => {
            this.errorHandler.handleError(error)
          }
        }
      )
    } else {
      const args = {
        id: 0,
        first_name: this.firstNameControl.value,
        last_name: this.lastNameControl.value,
        email: this.emailControl.value,
        phone: this.phoneControl.value,
        notes: this.notesControl.value
      }
      this.customerService.createCustomer(args).subscribe(
        {
          next: () => {
            this.dialogRef.close();
            window.location.reload();
          },
          error: (error) => {
            this.errorHandler.handleError(error)
          }
        }
      )
    }

  }
}
