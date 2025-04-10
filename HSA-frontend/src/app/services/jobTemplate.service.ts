import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { JobTemplateDataInterface } from '../interfaces/api-responses/jobTemplate.api.data.interface';

interface JobTemplateCreatePostData {
  description: string | null,
  name: string | null,
  services: [] | null,
  materials: [] | null
}

interface JobTemplateEditPostData {
  id: number | null,
  description: string | null,
  name: string | null,
}

interface JobTemplateDeletePostData {
  id: number | null,
}

interface JobTemplateServiceCreatePostData {
  jobTemplateID: number | null,
  services: [] | null
}

interface JobTemplateMaterialCreatePostData {
  jobTemplateID: number | null,
  materials: [] | null
}

interface JobTemplateJoinCreatePostData {
  type: string,
  id: number | null,
  addedItems: any | null
}

interface JobTemplateJoinDeletePostData {
  type: string,
  id: number | null,
  deletedItems: any | null
}

@Injectable({
  providedIn: 'root'
})
export class JobTemplateService {
  private apiGetUrl = `${environment.apiUrl}/api/get/jobtemplates`;
  private apiGetSpecificUrl = `${environment.apiUrl}/api/get/jobtemplate`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/jobtemplate`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/jobtemplate`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/jobtemplate`;
  responses: any[]  = []

  constructor(private http: HttpClient) {}

  public getJobTemplate(params?: Record<string, string | number>): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetUrl, { params: httpParams });
  }
  

  public createJobTemplate(data:JobTemplateCreatePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
  }

  public editJobTemplate(data:JobTemplateEditPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiEditUrl + `/${data.id}`, data);
  }

  public deleteJobTemplate(data:JobTemplateDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}`, data);
  }

  public getSpecificJobTemplateData(id: number | null): Observable<JobTemplateDataInterface> {
    return this.http.get<JobTemplateDataInterface>(this.apiGetSpecificUrl + `/${id}`);
  }

  public getJobTemplateService(id: number, params?: Record<string, string | number>): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetUrl + `/${id}/services`, { params: httpParams });
  }

  public createJobTemplateJoin(data: JobTemplateJoinCreatePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl + `/${data.id}/${data.type}`, data.addedItems);
  }

  public deleteJobTemplateJoin(data:JobTemplateJoinDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}/${data.type}s`, data.deletedItems);
  }
}
