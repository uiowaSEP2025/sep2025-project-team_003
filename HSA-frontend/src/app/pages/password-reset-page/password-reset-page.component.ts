import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ReactiveFormsModule, Validators, FormGroup, FormControl } from '@angular/forms';
import { MatInputModule, MatError } from '@angular/material/input';
import { passwordStrengthValidator, validateConfirmMatchesAndNotNull } from '../../utils/password-validators';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import { ConfirmPasswordResetServiceService } from '../../services/confirm-password-reset.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';

@Component({
  selector: 'app-password-reset-page',
  imports: [ReactiveFormsModule, MatInputModule, MatError, MatCardModule, MatButtonModule, PageTemplateComponent],
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

  constructor(private activatedRoute: ActivatedRoute, private passwordReset: ConfirmPasswordResetServiceService,
    private router: Router, private snackBar: MatSnackBar) { }



  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      this.token = params['token'];
    });
  }

  onSubmit() {
    if (!this.userAccountForm.valid) {
      this.userAccountForm.markAllAsTouched()
      return
    }

    this.passwordReset.confirmPasswordReset(this.userAccountForm.controls.password.value!, this.token).subscribe({
      next: (response) => {
        this.snackBar.open('Your password was reset successfully', '', {
          duration: 3000
        });
        this.router.navigate(['/login']);
      },
      error: (error) => {
        if (error.status === 404) {
          this.snackBar.open('Your token was invalid or expired, please try again later', '', {
            duration: 3000
          });

        }
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
