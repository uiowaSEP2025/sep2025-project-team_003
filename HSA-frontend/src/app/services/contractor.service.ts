import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';

interface ContractorCreatePostData {
  firstn: string | null
}

interface ContractorEditPostData {
  id: number | null,
}

interface ContractorDeletePostData {
  id: number | null,
}

@Injectable({
  providedIn: 'root'
})
export class ContractorService {
  private apiGetUrl = `${environment.apiUrl}/api/get/contractors`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/contractor`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/contractor`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/contractor`;
  responses: any[]  = []

  constructor(private http: HttpClient) {}

  public getContractor(params?: {[key: string]: string | number}): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetUrl, { params: httpParams });
  }
  

  public createContractor(data:ContractorCreatePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
  }

  public editContractor(data:ContractorEditPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiEditUrl + `/${data.id}`, data);
  }

  public deleteContractor(data:ContractorDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}`, data);
  }
}
