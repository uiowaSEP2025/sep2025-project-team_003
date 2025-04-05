import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatStepperModule } from '@angular/material/stepper';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButton } from '@angular/material/button';
import { MatOption, MatSelect } from '@angular/material/select';
import { HttpClient} from '@angular/common/http';
import { StateList } from '../../utils/states-list';

@Component({
  selector: 'app-signup-page',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatStepperModule,
    FormsModule,
    ReactiveFormsModule,
    MatButton,
    MatSelect,
    MatOption
  ],
  templateUrl: './signup-page.component.html',
  styleUrl: './signup-page.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})

export class SignupPageComponent implements OnInit {
  userAccountForm: FormGroup;
  registrationForm: FormGroup;
  states: any = []

  constructor(
    private router: Router, 
    private userAccountFormBuilder: FormBuilder,
    private registrationFormBuilder: FormBuilder, 
    private http: HttpClient
  ) {
    this.userAccountForm = this.userAccountFormBuilder.group({
      userFirstName: ['', Validators.required],
      userLastName: ['', Validators.required],
      userEmail: ['', [Validators.required, Validators.email]],
      username: ['', Validators.required],
      password: ['', Validators.required],
    });

    this.registrationForm = this.registrationFormBuilder.group({
      organizationName: ['', Validators.required],
      organizationEmail: ['', [Validators.required, Validators.email]],
      addressOne: ['', Validators.required],
      ownerName: ['', Validators.required],
      stateSelect: ['', Validators.required],
    });

    this.states = StateList.getStates()
  }

  ngOnInit() {
  }

  onSubmitUserCreation() {
    if (this.userAccountForm.invalid) {
      this.userAccountForm.markAllAsTouched();
    } else {
      this.registrationForm.patchValue({
        ownerName: this.userAccountForm.get('userFirstName')?.value + ' ' + this.userAccountForm.get('userLastName')?.value
      })
    }
  }

  onSubmitRegistration() {
    if (this.registrationForm.invalid) {
      this.registrationForm.markAllAsTouched();
      return;
    } else {
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
