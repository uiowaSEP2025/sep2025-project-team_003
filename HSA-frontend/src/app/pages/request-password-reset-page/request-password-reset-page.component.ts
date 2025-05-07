import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatError } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import { CommonModule } from '@angular/common';
import { RequestPasswordResetService } from '../../services/request-password-reset.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';


@Component({
  selector: 'app-request-password-reset-page',
  imports: [ReactiveFormsModule, MatError, MatInputModule, MatCardModule, MatButtonModule, CommonModule, PageTemplateComponent],
  templateUrl: './request-password-reset-page.component.html',
  styleUrl: './request-password-reset-page.component.scss',
  standalone: true
})
export class RequestPasswordResetPageComponent {

  email = new FormControl('', [Validators.email, Validators.required])
  matcher = new GenericFormErrorStateMatcher()

  constructor(private resetService: RequestPasswordResetService, private router: Router, private snackBar: MatSnackBar) {}

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }

  onSubmit() {
    if (this.email.invalid) {
      this.email.markAsTouched(); // trigger validation message
      return;
    }

    this.resetService.requestPasswordReset(this.email.value!).subscribe({
        next: () => {
          this.snackBar.open('If your email exists, an email will be sent', '', {
            duration: 3000
          });
          this.navigateToPage('login');
        },
        error: (error) => {
          console.error("Took an error on requesting the password token. This should never happen", error)
        }
    })

  }

}
