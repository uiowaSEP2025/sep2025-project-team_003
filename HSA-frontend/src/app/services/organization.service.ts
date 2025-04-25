import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import {Job} from '../interfaces/job.interface';

interface CreateOrganizationPostData {
  org_name: string | null
  org_email: string | null
  org_city : string | null
  org_state: string | null
  org_zip: string | null
  org_address: string | null
  org_phone: string | null
  org_owner_first_name: string | null
  org_owner_last_name: string | null
  owning_user: string | null
  is_onboarding: boolean | null
  default_labor_rate: number | null
  default_payment_link: string | null
}

interface OnboardingUpdatePostData {
	customerRequest: any | null
	serviceRequest: any | null
	materialRequest: any | null
	contractorRequest: any | null
	isOnboarding: boolean | null
}

@Injectable({
	providedIn: 'root'
})

export class OrganizationService {
	private apiGetUrl = `${environment.apiUrl}/api/get/organization`;
	private apiCreateUrl = `${environment.apiUrl}/api/create/organization`;
	private apiEditUrl = `${environment.apiUrl}/api/edit/organization`;
	private apiOnboardingUpdateUrl = `${environment.apiUrl}/api/edit/organization/onboarding`;
	private apiDeleteUrl = `${environment.apiUrl}/api/delete/organization`

	constructor(private http: HttpClient) { }

	public createOrganization(data: CreateOrganizationPostData): Observable<StandardApiResponse> {
		return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
	}

	public getOrganization(): Observable<StandardApiResponse> {
		return this.http.get<StandardApiResponse>(this.apiGetUrl);
	}

	public editOrganization(data: CreateOrganizationPostData): Observable<StandardApiResponse> {
		return this.http.post<StandardApiResponse>(this.apiEditUrl, data);
	}

	public updateOnboardingProcess(data: OnboardingUpdatePostData): Observable<StandardApiResponse> {
		return this.http.post<StandardApiResponse>(this.apiOnboardingUpdateUrl, data);
	}

}
