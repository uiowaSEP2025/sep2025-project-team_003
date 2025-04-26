import { Component } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { CustomerService } from '../../../services/customer.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-customer-page',
  imports: [FormsModule, MatInputModule, ReactiveFormsModule, MatButtonModule, MatIconModule],
  templateUrl: './create-customer-page.component.html',
  styleUrl: './create-customer-page.component.scss'
})
export class CreateCustomerPageComponent {
  constructor(private customerService: CustomerService, private router: Router) { }

  firstNameControl = new FormControl('', Validators.required)
  lastNameControl = new FormControl('', Validators.required)
  emailControl = new FormControl('', [Validators.email, Validators.required])
  phoneControl = new FormControl('', Validators.required)
  notesControl = new FormControl('')
  matcher = new GenericFormErrorStateMatcher()

  private isFormValid() {
    if (
      this.firstNameControl.valid &&
      this.lastNameControl.valid &&
      this.emailControl.valid &&
      this.phoneControl.valid) {
      return true
    }
    return false
  }

  onSubmit() {
    if (!this.isFormValid()) {
      return
    }
    const data = {
      first_name: this.firstNameControl.value,
      last_name: this.lastNameControl.value,
      email: this.emailControl.value,
      phone: this.phoneControl.value,
      notes: this.notesControl.value
    }

    this.customerService.createCustomer(data).subscribe(
      {next: (response) => {
        this.router.navigate(['/customers']);
      },
      error: (error) => {
      }}
    )
  }

}
