import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Customer, CustomerParams } from '../interfaces/customer.interface';
import { TableApiResponse } from '../interfaces/api-responses/table.api.interface';

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
  private apiGetExcludedUrl = `${environment.apiUrl}/api/get/customers/exclude`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/customer`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/customer`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/customer`;
  responses: any[]  = []

  constructor(private http: HttpClient) {}

  public getCustomer(params?: Record<string, string | number>): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetUrl, { params: httpParams });
  }

  public getExcludedCustomer(params?: CustomerParams): Observable<TableApiResponse<Customer>> {
      let httpParams = new HttpParams();
  
      // Add query parameters
      if (params?.excludeIDs) {
        params.excludeIDs.forEach(id => {
          httpParams = httpParams.append('excludeIDs', id.toString());
        });
      }
  
      if (params) {
        Object.keys(params).forEach(key => {
          if (key !== 'excludeIDs') {
            const value = params[key as keyof CustomerParams];
            if (value !== undefined) {
              httpParams = httpParams.append(key, value.toString());
            }
          }
        });
      }
  
      return this.http.get<TableApiResponse<Customer>>(this.apiGetExcludedUrl, { params: httpParams });
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
