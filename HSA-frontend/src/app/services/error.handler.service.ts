import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root',
})
export class ErrorHandlerService {

  constructor(private router: Router, private snackBar: MatSnackBar) {
  }

  // handles api errors
  handleError(error: HttpErrorResponse, prevPath = 'home'): void {
    if (error.status === 401) {
      this.snackBar.open('Please login to the system', '', {
        duration: 3000
      });
      this.router.navigate(['/login'], { queryParams: { prevPath: prevPath }});
    } else if (error.status === 404) {
      this.router.navigate(['/404']);
    }
  }
}
