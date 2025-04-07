import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Service, ServiceParams } from '../interfaces/service.interface';
import { TableApiResponse } from '../interfaces/api-responses/table.api.interface';

interface ServiceCreatePostData {
  service_name: string | null
  service_description: string | null
  default_hourly_rate: number | null
}

interface ServiceEditPostData {
  id: number | null,
  service_name: string | null
  service_description: string | null
  default_hourly_rate: number | null
}

interface ServiceDeletePostData {
  id: number | null,
  service_name: string | null
}

@Injectable({
  providedIn: 'root'
})
export class ServiceService {
  private apiGetUrl = `${environment.apiUrl}/api/get/services`;
  private apiGetExcludedUrl = `${environment.apiUrl}/api/get/services/exclude`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/service`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/service`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/service`;


  constructor(private http: HttpClient) {}

  public getService(params?: Record<string, string | number>): Observable<TableApiResponse<Service>> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<TableApiResponse<Service>>(this.apiGetUrl, { params: httpParams });
  }

  public getExcludedService(params?: ServiceParams): Observable<TableApiResponse<Service>> {
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
          const value = params[key as keyof ServiceParams];
          if (value !== undefined) {
            httpParams = httpParams.append(key, value.toString());
          }
        }
      });
    }

    return this.http.get<TableApiResponse<Service>>(this.apiGetExcludedUrl, { params: httpParams });
  }


  public createService(data:ServiceCreatePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
  }

  public editService(data:ServiceEditPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiEditUrl + `/${data.id}`, data);
  }

  public deleteService(data:ServiceDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}`, data);
  }
}
