import { Component } from '@angular/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatButtonModule} from '@angular/material/button';
import {
  FormControl,
  Validators,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import {MatSnackBar} from '@angular/material/snack-bar';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import { UserAuthService } from '../../services/user-auth.service';
import { ErrorHandlerService } from '../../services/error.handler.service';

@Component({
  selector: 'app-login',
  imports: [FormsModule, MatFormFieldModule, MatInputModule, MatButtonModule,ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  matcher = new GenericFormErrorStateMatcher();
  usernameFormControl = new FormControl('', [Validators.required]);
  passwordFormControl = new FormControl('', [Validators.required]);

  constructor(private authService: UserAuthService, private snackBar: MatSnackBar, private errorHandler: ErrorHandlerService) {}

  onSubmit() {
    if (this.usernameFormControl.valid && this.passwordFormControl.valid) {
      this.authService.login({
        username: this.usernameFormControl.value,
        password: this.passwordFormControl.value
      }).subscribe({
        next: () => {
          this.snackBar.open('Login Successful', '', {
            duration: 3000
          });
        },
        error: (error) => {
          this.errorHandler.handleError(error)
        }
      });
    }
  }
}
