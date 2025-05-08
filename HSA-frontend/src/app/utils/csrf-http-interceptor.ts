import { HttpRequest, HttpHandlerFn, HttpEvent } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../environments/environment";

export function getCSRFToken(): string {
    const match = document.cookie.match(/(?:^|;)\s*csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
}

export function csrfInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
    if (environment.requireCSRF) {
        const csrfToken = getCSRFToken();
        if (!csrfToken) {
            console.error("ERROR: could not grab the csrf token from cookies!")
        }
        req = req.clone({
            setHeaders: {
                "X-CSRFToken": csrfToken
            }
        });
    }
    return next(req);
}