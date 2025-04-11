import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {StandardApiResponse} from '../interfaces/api-responses/standard-api-response.interface';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  constructor(private http: HttpClient) {}

  getData(
    modelName: string,
    page = 1,
    pageSize = 10,
    searchTerm = '',
    orderBy = '',
    filters: any = {}
  ): Observable<any> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());

    if (searchTerm) {
      params = params.set('search', searchTerm);
    }

    if (orderBy) {
      params = params.set('order_by', orderBy);
    }

    // Add any additional filters
    Object.keys(filters).forEach(key => {
      params = params.set(key, filters[key]);
    });

    return this.http.get(`/api/get/${modelName}s`, { params });
  }

  public view(id: number, modelName: string): Observable<any> {
    return this.http.get(`/api/get/${modelName}/${id}`)
  }

  public edit(data, modelName: string): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(`/api/edit/${modelName}/${data.id}`, data);
  }


}
