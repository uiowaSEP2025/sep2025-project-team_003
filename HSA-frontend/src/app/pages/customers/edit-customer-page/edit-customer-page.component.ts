import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatFormFieldModule, } from '@angular/material/form-field';
import { ReactiveFormsModule, FormControl, Validators, FormsModule } from '@angular/forms';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { CustomerService } from '../../../services/customer.service';
import { Router } from '@angular/router';
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
  notes!: string

  constructor(private activatedRoute: ActivatedRoute, private customerService: CustomerService, private router: Router) { }

  firstNameControl = new FormControl('', Validators.required)
  lastNameControl = new FormControl('', Validators.required)
  emailControl = new FormControl('', [Validators.email, Validators.required])
  phoneControl = new FormControl('', Validators.required)
  notesControl = new FormControl('')
  matcher = new GenericFormErrorStateMatcher()

  // Format phone number from xxxxxxxxxx to xxx-xxx-xxxx
  private formatPhoneNumber(phone: string): string {
    if (!phone) return '';
    // Remove any non-digit characters
    const cleaned = phone.replace(/\D/g, '');
    // Check if we have 10 digits
    if (cleaned.length === 10) {
      return `${cleaned.slice(0, 3)}-${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
    }
    return phone; // Return original if not 10 digits
  }

  ngOnInit() {
    // pass existing field in as a query param
    this.activatedRoute.queryParams.subscribe(params => {
      this.email = params['email'];
      this.firstName = params['first_name'];
      this.lastName = params['last_name'];
      this.phoneNo = params['phone'];
      this.notes = params['notes'];
      this.firstNameControl.setValue(this.firstName);
      this.lastNameControl.setValue(this.lastName);
      this.emailControl.setValue(this.email);
      this.phoneControl.setValue(this.formatPhoneNumber(this.phoneNo));
      this.notesControl.setValue(this.notes);
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
      notes: this.notesControl.value
    }
    this.customerService.editCustomer(args).subscribe(
      {
        next: (response) => {
          this.router.navigate(['/customers']);
        },
        error: (error) => {
        }
      }
    )
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
