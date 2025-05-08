import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';

interface CreateOrganizationPostData {
	name: string | null
	email: string | null
	city: string | null
	phone: string | null
	requestorState: string | null
	requestorZip: string | null
	requestorAddress: string | null
	ownerFn: string | null
	ownerLn: string | null
}

interface GetURLResponse {
	URL: string
}

interface SetURLData {
	url: string | null
}

interface OnboardingUpdatePostData {
	customerRequest: any | null
	serviceRequest: any | null
	materialrRequest: any | null
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
	private getPaymentURL = `${environment.apiUrl}/api/get/payment-link`
	private setPaymentURL = `${environment.apiUrl}/api/set/payment-link`
	
	constructor(private http: HttpClient) { }

	public getPayemntLink():Observable<GetURLResponse> {
		return this.http.get<GetURLResponse>(this.getPaymentURL);
	}

	public setPayemntLink(data: SetURLData):Observable<any> {
		return this.http.post(this.setPaymentURL, data);
	}

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
