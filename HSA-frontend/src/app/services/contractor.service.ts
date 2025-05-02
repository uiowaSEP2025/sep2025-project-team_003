import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { TableApiResponse } from '../interfaces/api-responses/table.api.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Contractor, ContractorParams } from '../interfaces/contractor.interface';
import { environment } from '../../environments/environment';

export interface ContractorNameId {
  name: string,
  id: number
}

interface ContractorCreatePostData {
  firstName: string | null
  lastName: string | null
  email: string | null
  phone: string | null
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
  private apiGetAllUrl = `${environment.apiUrl}/api/get/all/contractors`;
  private apiGetExcludedUrl = `${environment.apiUrl}/api/get/contractors/exclude`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/contractor`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/contractor`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/contractor`;

  constructor(private http: HttpClient) {}

  public getAllContractors():Observable<ContractorNameId[]> {
    return this.http.get<ContractorNameId[]>(this.apiGetAllUrl);
  }

  public getContractor(params?: Record<string, string | number>): Observable<TableApiResponse<Contractor>> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<TableApiResponse<Contractor>>(this.apiGetUrl, { params: httpParams });
  }

  public getExcludedContractor(params?: ContractorParams): Observable<TableApiResponse<Contractor>> {
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
            const value = params[key as keyof ContractorParams];
            if (value !== undefined) {
              httpParams = httpParams.append(key, value.toString());
            }
          }
        });
      }

      return this.http.get<TableApiResponse<Contractor>>(this.apiGetExcludedUrl, { params: httpParams });
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
