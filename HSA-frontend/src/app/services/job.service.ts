import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { JobDataInterface } from '../interfaces/api-responses/job.api.data.interface';
import { Job, JobParams } from '../interfaces/job.interface';
import { TableApiResponse } from '../interfaces/api-responses/table.api.interface';
import JobSimplified from '../interfaces/job_data.interface';

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
  jobStatus: string | null,
  startDate: string | null,
  endDate: string | null,
  description: string | null,
  customerID: number | null,
  city: string | null,
  state: string | null,
  zip: string | null,
  address: string | null,
}

interface JobDeletePostData {
  id: number | null,
}

interface JobJoinCreatePostData {
  type: string,
  id: number | null,
  addedItems: any | null
}

interface JobJoinDeletePostData {
  type: string,
  id: number | null,
  deletedItems: any | null
}

@Injectable({
  providedIn: 'root'
})
export class JobService {
  private apiGetUrl = `${environment.apiUrl}/api/get/jobs`;
  private apiGetExcludedUrl = `${environment.apiUrl}/api/get/jobs/exclude`;
  private apiGetSpecificUrl = `${environment.apiUrl}/api/get/job`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/job`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/job`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/job`;
  private getJobsByContractorUrl = `${environment.apiUrl}/api/get/jobs/by-contractor`
  responses: any[]  = []

  constructor(private http: HttpClient) {}

  public getJobsByContractor(contractorID: number, search: string, pageSize: number, offset: number): Observable<TableApiResponse<JobSimplified>> {
    const searchquery = search === "" ? "" : `search=${search}&`
    return this.http.get<TableApiResponse<JobSimplified>>(`${this.getJobsByContractorUrl}?${searchquery}pagesize=${pageSize}&offset=${offset}&contractor=${contractorID}`);
  }

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

   public getExcludedJob(params?: JobParams): Observable<TableApiResponse<Job>> {
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
          const value = params[key as keyof JobParams];
          if (value !== undefined) {
            httpParams = httpParams.append(key, value.toString());
          }
        }
      });
    }

    return this.http.get<TableApiResponse<Job>>(this.apiGetExcludedUrl, { params: httpParams });
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

  public getSpecificJobData(id: number | null): Observable<JobDataInterface> {
    return this.http.get<JobDataInterface>(this.apiGetSpecificUrl + `/${id}`);
  }

  public getJobService(id: number, params?: Record<string, string | number>): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetUrl + `/${id}/services`, { params: httpParams });
  }

  public createJobJoin(data: JobJoinCreatePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl + `/${data.id}/${data.type}`, data.addedItems);
  }

  public deleteJobJoin(data:JobJoinDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}/${data.type}s`, data.deletedItems);
  }
}
