import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatFormFieldModule, } from '@angular/material/form-field';
import { ReactiveFormsModule, FormControl, Validators, FormsModule } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { CustomerService } from '../../../services/customer.service';
import { Router } from '@angular/router';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-edit-customer-page',
  imports: [
    MatFormFieldModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    FormsModule
  ],
  templateUrl: './edit-customer-page.component.html',
  styleUrl: './edit-customer-page.component.scss'
})
export class EditCustomerPageComponent implements OnInit {
  email!: string
  firstName!: string
  lastName!: string
  phoneNo!: string
  custId: number | null = null


  constructor(private activatedRoute: ActivatedRoute, private customerService: CustomerService, private router: Router, private errorHandler: ErrorHandlerService) { }

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
      this.firstName = params['first_name'];
      this.lastName = params['last_name'];
      this.phoneNo = params['phone_no'];
      this.firstNameControl.setValue(this.firstName);
      this.lastNameControl.setValue(this.lastName);
      this.emailControl.setValue(this.email);
      this.phoneControl.setValue(this.phoneNo);
    });

    this.activatedRoute.paramMap.subscribe(params => {
      this.custId = Number(params.get('id'));
    })
  }

  private isFormValid(): boolean {
    if (this.firstNameControl.valid &&
      this.lastNameControl.valid &&
      this.emailControl.valid &&
      this.phoneControl.valid &&
      this.notesControl) {
      return true
    }
    return false
  }

  handleSave() {
    if (!this.isFormValid()) {
      return
    }
    const args = {
      id: this.custId,
      firstn: this.firstNameControl.value,
      lastn: this.lastNameControl.value,
      email: this.emailControl.value,
      phoneno: this.phoneControl.value,
      notes: this.phoneControl.value
    }
    this.customerService.editCustomer(args).subscribe(
      {
        next: (response) => {
          this.router.navigate(['/customers']);
        },
        error: (error) => {
          this.errorHandler.handleError(error)
        }
      }
    )
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
