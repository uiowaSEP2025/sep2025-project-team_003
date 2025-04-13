import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { UserAuthService } from './user-auth.service';

@Injectable({
  providedIn: 'root',
})
export class ErrorHandlerService {

  constructor(private router: Router, private snackBar: MatSnackBar, private userAuth: UserAuthService) {
  }

  // handles api errors
  handleError(error: HttpErrorResponse, prevPath: string = 'home'): void {
    if (error.status === 401) {
      this.userAuth.setLoginStatus(false)
      this.snackBar.open('Please login to the system', '', {
        duration: 3000
      });
      this.router.navigate(['/login'], { queryParams: { prevPath: prevPath }});
    } else if (error.status === 404) {
      this.router.navigate(['/404']);
    }
  }
}
