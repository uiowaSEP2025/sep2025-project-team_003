import { Injectable } from '@angular/core';
import {
    HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable()
export class RedirectInterceptor implements HttpInterceptor {
    constructor(private router: Router) { }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(req).pipe(
            catchError((err: HttpErrorResponse) => {
                console.error(`HTTP Error: ${err.status} ${err.message}`);

                if (err.status === 401) {
                    this.router.navigate(['/login']);
                } else if (err.status === 404) {
                    this.router.navigate(['/not-found']);
                } else if (err.status >= 500) {
                    this.router.navigate(['/server-error']);
                }

                return throwError(() => err);
            })
        );
    }
}
