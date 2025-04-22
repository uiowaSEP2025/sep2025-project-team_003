import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { TableApiResponse } from '../interfaces/api-responses/table.api.interface';
import { Request, RequestParams } from '../interfaces/request.interface';
import { RequestData } from '../interfaces/api-responses/request.api.interface';

interface RequestCreatePostData {

}

interface RequestEditPostData {
    id: number | null
}

interface RequestDeletePostData {
    id: number | null
}

@Injectable({
  providedIn: 'root'
})
export class RequestService {
  private apiGetUrl = `${environment.apiUrl}/api/get/requests`;
  private apiGetExcludedUrl = `${environment.apiUrl}/api/get/requests/exclude`;
  private apiGetSpecificUrl = `${environment.apiUrl}/api/get/request`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/request`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/request`;
  private apiApproveUrl = `${environment.apiUrl}/api/approve/request`;
  private apiDenyUrl = `${environment.apiUrl}/api/delete/request`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/request`;
  responses: any[]  = []

  constructor(private http: HttpClient) {}

  public getRequest(params?: Record<string, string | number>): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetUrl, { params: httpParams });
  }
  
   public getExcludedRequest(params?: RequestParams): Observable<TableApiResponse<Request>> {
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
          const value = params[key as keyof RequestParams];
          if (value !== undefined) {
            httpParams = httpParams.append(key, value.toString());
          }
        }
      });
    }

    return this.http.get<TableApiResponse<Request>>(this.apiGetExcludedUrl, { params: httpParams });
  }

  public createRequest(data: RequestCreatePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
  }

  public editRequest(data: RequestEditPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiEditUrl + `/${data.id}`, data);
  }

  public approveDenyRequest(data: RequestDeletePostData, isApproved: boolean): Observable<StandardApiResponse> {
    console.log(data, isApproved)
    return isApproved
      ? this.http.post<StandardApiResponse>(this.apiApproveUrl + `/${data.id}`, data)
      : this.http.post<StandardApiResponse>(this.apiDenyUrl + `/${data.id}`, data)
  } 

  public deleteRequest(data: RequestDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}`, data);
  }

  public getSpecificRequestData(id: number | null): Observable<RequestData> {
    return this.http.get<RequestData>(this.apiGetSpecificUrl + `/${id}`);
  }
}
