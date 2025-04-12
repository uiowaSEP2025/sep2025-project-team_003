import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ReactiveFormsModule, Validators, FormGroup, FormControl } from '@angular/forms';
import { MatInputModule, MatError } from '@angular/material/input';
import { passwordStrengthValidator, validateConfirmMatchesAndNotNull } from '../../utils/password-validators';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';

@Component({
  selector: 'app-password-reset-page',
  imports: [ReactiveFormsModule, MatInputModule, MatError, MatCardModule, MatButtonModule],
  templateUrl: './password-reset-page.component.html',
  styleUrl: './password-reset-page.component.scss'
})
export class PasswordResetPageComponent implements OnInit {

  private token!: string
  matcher = new GenericFormErrorStateMatcher()

  userAccountForm = new FormGroup({
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
      Validators.maxLength(16),
      passwordStrengthValidator
    ]),
    confirmPassword: new FormControl('',)
  }, validateConfirmMatchesAndNotNull);

  constructor(private activatedRoute: ActivatedRoute) { }



  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      this.token = params['token'];
    });
  }

  onSubmit() {
    console.log(this.userAccountForm.controls.confirmPassword.value)
    if (!this.userAccountForm.valid) {
      this.userAccountForm.markAllAsTouched()
    }

  }

}
