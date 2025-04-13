import { Component } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { FormControl, Validators, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import { UserAuthService } from '../../services/user-auth.service';
import { MatCardModule } from '@angular/material/card';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [
    FormsModule, 
    MatFormFieldModule, 
    MatInputModule, 
    MatButtonModule,
    MatCardModule,
    ReactiveFormsModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  previousUrlPath: string = 'home'
  matcher = new GenericFormErrorStateMatcher();
  usernameFormControl = new FormControl('', [Validators.required]);
  passwordFormControl = new FormControl('', [Validators.required]);

  constructor(private router: Router, private route: ActivatedRoute, private authService: UserAuthService, private snackBar: MatSnackBar) {
    this.route.queryParams.subscribe(params => {
      if (params['prevPath'] !== undefined) {
        this.previousUrlPath = params['prevPath']
      }
    })
  }

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

          if (this.previousUrlPath === 'login') {
            this.previousUrlPath = 'home'
          }
          
          this.navigateToPage(`/${this.previousUrlPath}`)
        },
        error: (error) => {
          if (error.status === 401) {
            this.snackBar.open('Username or password is invalid, please try again!', '', {
              duration: 3000
            });
          } else {
          }
        }
      });
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`])
  }
}
