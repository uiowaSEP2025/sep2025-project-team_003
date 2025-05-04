import { Component, OnInit } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import { MatCardModule } from '@angular/material/card';
import { ContractorService } from '../../../services/contractor.service';

@Component({
  selector: 'app-edit-contractors-page',
  imports: [
    MatFormFieldModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    FormsModule
  ],
  templateUrl: './edit-contractors-page.component.html',
  styleUrl: './edit-contractors-page.component.scss'
})
export class EditContractorsPageComponent implements OnInit {
  email!: string
  firstName!: string
  lastName!: string
  phoneNo!: string
  custId: number | null = null

  constructor(private activatedRoute: ActivatedRoute, private router: Router, private contractorService: ContractorService) { }
  firstNameControl = new FormControl('', Validators.required)
  lastNameControl = new FormControl('', Validators.required)
  emailControl = new FormControl('', [Validators.email, Validators.required])
  phoneControl = new FormControl('', Validators.required)
  matcher = new GenericFormErrorStateMatcher()


  ngOnInit() {
    // pass existing field in as a query param
    this.activatedRoute.queryParams.subscribe(params => {
      this.email = params['email'];
      this.firstName = params['first_name'];
      this.lastName = params['last_name'];
      this.phoneNo = params['phone'];
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
      this.phoneControl.valid)
    {
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
      first_name: this.firstNameControl.value,
      last_name: this.lastNameControl.value,
      email: this.emailControl.value,
      phone: this.phoneControl.value,
    }
    this.contractorService.editContractor(args).subscribe(
      {
        next: (response) => {
          this.router.navigate(['/contractors']);
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
