import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';

interface CustomerCreatePostData {
  firstn: string | null
  lastn: string | null
  email: string | null
  phoneno: string | null
  notes: string | null
}

interface CustomerEditPostData {
  id: number | null,
  firstn: string | null
  lastn: string | null
  email: string | null
  phoneno: string | null
  notes: string | null
}

interface CustomerDeletePostData {
  id: number | null,
  firstn: string | null
  lastn: string | null
}

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  private apiGetUrl = `${environment.apiUrl}/api/get/customers`;
    private apiCreateUrl = `${environment.apiUrl}/api/create/customer`;
    private apiEditUrl = `${environment.apiUrl}/api/edit/customer`;
    private apiDeleteUrl = `${environment.apiUrl}/api/delete/customer`;
    responses: any[]  = []
  
    constructor(private http: HttpClient) {}
  
    public getCustomer(params?: {[key: string]: string | number}): Observable<StandardApiResponse> {
      let httpParams = new HttpParams();
  
      // Add query parameters
      if (params) {
        Object.keys(params).forEach(key => {
          httpParams = httpParams.append(key, params[key])
        })
      }
  
      return this.http.get<StandardApiResponse>(this.apiGetUrl, { params: httpParams });
    }
    
  
    public createCustomer(data:CustomerCreatePostData): Observable<StandardApiResponse> {
      return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
    }
  
    public editCustomer(data:CustomerEditPostData): Observable<StandardApiResponse> {
      return this.http.post<StandardApiResponse>(this.apiEditUrl + `/${data.id}`, data);
    }
  
    public deleteCustomer(data:CustomerDeletePostData): Observable<StandardApiResponse> {
      return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}`, data);
    }
}
