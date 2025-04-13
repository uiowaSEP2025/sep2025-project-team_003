import { HttpRequest, HttpHandlerFn, HttpEvent, HttpErrorResponse, HttpResponse } from "@angular/common/http";
import { Observable, catchError, tap, throwError } from "rxjs";
import { inject } from "@angular/core";
import { Router } from "@angular/router";
import { UserAuthService } from "../services/user-auth.service";

export function RedirectAndAuthInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
    const router = inject(Router);
    const userAuth = inject(UserAuthService)

    return next(req).pipe(
        tap(event => {
            if (event instanceof HttpResponse) {
                const status = event.status;
                if (status >= 200 && status < 300) {
                    // we are logged in
                    userAuth.setLoginStatus(true)
                    
                } else if (status >= 300 && status < 400) {
                    
                }
            }
        }),

        catchError((err: HttpErrorResponse) => {
            const url = req.url;

            console.error(`Calling to endpoint ${url} failed with status code ${err.status}, message: ${err.message}`);

            if (err.status === 401) {
                router.navigate(['/login'], {
                    queryParams: {
                      prevpath: 'value1',
                    }
                  });
            } else if (err.status === 403) {
                switch (err.error.reason) {
                case "onboarding":
                    router.navigateByUrl("/onboarding");
                    break;
                default:
                    console.log("Unknown fruit");
                    break;
                }
            } else if (err.status === 404) {
                router.navigateByUrl("/404");
            } else if (err.status >= 500) {
                router.navigateByUrl("/500");
            }

            return throwError(() => err);
        })
    );
}
