import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ErrorHandlerService {

  constructor(private router: Router) {
  }

  // handles api errors
  handleError(error: HttpErrorResponse, prevPath: string = 'home'): void {
    if (error.status === 401) {
      this.router.navigate(['/login'], { queryParams: { prevPath: prevPath }});
    } else if (error.status === 404) {
      this.router.navigate(['/404']);
    }
  }
}
