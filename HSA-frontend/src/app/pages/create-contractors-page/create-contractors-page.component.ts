import { Component } from '@angular/core';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import { FormControl,ReactiveFormsModule,FormsModule, Validators } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButton } from '@angular/material/button';
import { ContractorService } from '../../services/contractor.service';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-create-contractors-page',
  imports: [MatInputModule,ReactiveFormsModule,FormsModule, MatButton, MatCardModule],
  templateUrl: './create-contractors-page.component.html',
  styleUrl: './create-contractors-page.component.scss'
})
export class CreateContractorsPageComponent {
  constructor(private contractorService: ContractorService, private router: Router) { }

  firstNameControl = new FormControl('', Validators.required)
  lastNameControl = new FormControl('', Validators.required)
  emailControl = new FormControl('', [Validators.email, Validators.required])
  phoneControl = new FormControl('', Validators.required)
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
      firstName: this.firstNameControl.value,
      lastName: this.lastNameControl.value,
      email: this.emailControl.value,
      phone: this.phoneControl.value,
    }

    this.contractorService.createContractor(data).subscribe(
      {next: (response) => {
        this.router.navigate(['/contractors']);
      },
      error: (error) => {
      }}
    )
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
