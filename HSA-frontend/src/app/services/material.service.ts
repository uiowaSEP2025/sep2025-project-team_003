import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { StandardApiResponse } from '../interfaces/standard-api-response.interface';

interface MaterialCreatePostData {
  material_name: string | null
}

interface MaterialEditPostData {
  id: number | null,
  material_name: string | null
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
  private apiCreateUrl = `${environment.apiUrl}/api/create/material`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/material`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/material`;
  responses: any[]  = []

  constructor(private http: HttpClient) {}

  public getMaterial(params?: {[key: string]: string | number}): Observable<StandardApiResponse> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<StandardApiResponse>(this.apiGetUrl, { params: httpParams });
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
