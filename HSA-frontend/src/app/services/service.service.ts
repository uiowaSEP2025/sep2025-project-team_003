import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';

interface ServiceCreatePostData {
  service_name: string | null
  service_description: string | null
}

interface ServiceEditPostData {
  id: number | null,
  service_name: string | null
  service_description: string | null
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
    private apiCreateUrl = `${environment.apiUrl}/api/create/service`;
    private apiEditUrl = `${environment.apiUrl}/api/edit/service`;
    private apiDeleteUrl = `${environment.apiUrl}/api/delete/service`;
    responses: any[]  = []
  
    constructor(private http: HttpClient) {}
  
    public getService(params?: Record<string, string | number>): Observable<StandardApiResponse> {
      let httpParams = new HttpParams();
  
      // Add query parameters
      if (params) {
        Object.keys(params).forEach(key => {
          httpParams = httpParams.append(key, params[key])
        })
      }
  
      return this.http.get<StandardApiResponse>(this.apiGetUrl, { params: httpParams });
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
