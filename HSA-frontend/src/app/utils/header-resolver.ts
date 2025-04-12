import { Injectable } from "@angular/core";
import { ActivatedRouteSnapshot, Resolve, Router, RouterStateSnapshot } from "@angular/router";
import { OrganizationService } from "../services/organization.service";
import { catchError, map, Observable, of } from "rxjs";

@Injectable({ providedIn: 'root' })
export class HeaderResolver implements Resolve<any> {
  constructor(
    private organizationService: OrganizationService,
    private router: Router
  ) {}

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<{ organization?: any }> {
    return this.organizationService.getOrganization().pipe(
      map((organization: any) => {
        if (organization["is_onboarding"] && !state.url.includes('onboarding')) {
          this.router.navigate(['/onboarding']);
        }
        return { organization };
      }),
      catchError(error => {
        return of({ organization: null });
      })
    );
  }
}