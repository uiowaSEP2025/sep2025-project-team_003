import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ErrorHandlerService {
  constructor(private router: Router) {}

  handleError(error: HttpErrorResponse): void {
    if (error.status === 401) {
      this.router.navigate(['/login']);
    } else if (error.status === 404) {
      this.router.navigate(['/404']);
    }
  }
}
