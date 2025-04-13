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
	isOnboarding: boolean | null
}

@Injectable({
	providedIn: 'root'
})

export class OrganizationService {
	private apiGetUrl = `${environment.apiUrl}/api/get/organization`;
	private apiCreateUrl = `${environment.apiUrl}/api/create/organization`;
	private apiEditUrl = `${environment.apiUrl}/api/edit/organization`;
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
}
