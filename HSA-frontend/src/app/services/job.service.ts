import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { JobDataInterface } from '../interfaces/api-responses/job.api.data.interface';

interface JobCreatePostData {
  jobStatus: string | null,
  startDate: string | null,
  endDate: string | null,
  description: string | null,
  customerID: number | null,
  city: string | null,
  state: string | null,
  zip: string | null,
  address: string | null,
  contractors: [] | null,
  services: [] | null,
  materials: [] | null
}

interface JobEditPostData {
  id: number | null,

}

interface JobDeletePostData {
  id: number | null,
}

@Injectable({
  providedIn: 'root'
})
export class JobService {
  private apiGetUrl = `${environment.apiUrl}/api/get/jobs`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/job`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/job`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/job`;
  private apiSpecificUrl = `${environment.apiUrl}/api/get/job`;
  private apiGetJobService = `${environment.apiUrl}/api/get/job`;
  responses: any[]  = []

  constructor(private http: HttpClient) {}

  public getJob(params?: Record<string, string | number>): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetUrl, { params: httpParams });
  }
  

  public createJob(data:JobCreatePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
  }

  public editJob(data:JobEditPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiEditUrl + `/${data.id}`, data);
  }

  public deleteJob(data:JobDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}`, data);
  }

  public getSpecificJobData(id: number): Observable<JobDataInterface> {
    return this.http.get<JobDataInterface>(this.apiSpecificUrl + `/${id}`);
  }

  public getJobService(id: number, params?: Record<string, string | number>): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetJobService + `/${id}/services`, { params: httpParams });
  }
}
