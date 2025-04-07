import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { TableApiResponse } from '../interfaces/api-responses/table.api.interface';
import { Material, MaterialParams } from '../interfaces/material.interface';

interface MaterialCreatePostData {
  material_name: string | null
  material_description: string | null
  default_cost: number | null
}

interface MaterialEditPostData {
  id: number | null,
  material_name: string | null
  material_description: string | null
  default_cost: number | null
}

interface MaterialDeletePostData {
  id: number | null,
  material_name: string | null
}

@Injectable({
  providedIn: 'root'
})
export class MaterialService {
  private apiGetUrl = `${environment.apiUrl}/api/get/materials`;
  private apiGetExcludedUrl = `${environment.apiUrl}/api/get/materials/exclude`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/material`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/material`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/material`;

  constructor(private http: HttpClient) {}

  public getMaterial(params?: Record<string, string | number>): Observable<TableApiResponse<Material>> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<TableApiResponse<Material>>(this.apiGetUrl, { params: httpParams });
  }

  public getExcludedMaterial(params?: MaterialParams): Observable<TableApiResponse<Material>> {
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
          const value = params[key as keyof MaterialParams];
          if (value !== undefined) {
            httpParams = httpParams.append(key, value.toString());
          }
        }
      });
    }

    return this.http.get<TableApiResponse<Material>>(this.apiGetExcludedUrl, { params: httpParams });
  }

  public createMaterial(data:MaterialCreatePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
  }

  public editMaterial(data:MaterialEditPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiEditUrl + `/${data.id}`, data);
  }

  public deleteMaterial(data:MaterialDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}`, data);
  }
}
