// pagination.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import {StandardApiResponse} from '../interfaces/api-responses/standard-api-response.interface'; // Assume you have an auth service

interface PaginationResponse<T> {
  data: T[];
  total_items: number;
  total_pages: number;
  current_page: number;
}

@Injectable({
  providedIn: 'root'
})
export class PaginationService {
  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {
  }

  getPaginatedData<T>(
    endpoint: string,
    page: number = 1,
    pageSize: number = 10,
    searchTerm: string = '',
    filters: any = {}
  ): Observable<PaginationResponse<T>> {
    // Get current user ID from auth service
    const userId = this.authService.getCurrentUserId();

    // Build query parameters
    let params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString())
      .set('user_id', userId.toString());

    if (searchTerm) {
      params = params.set('search', searchTerm);
    }

    // Add any additional filters
    Object.keys(filters).forEach(key => {
      params = params.set(key, filters[key]);
    });

    return this.http.get<PaginationResponse<T>>(endpoint, {params});
  }

  public view(id: number, modelName: string): Observable<any> {
    return this.http.get(`/api/get/${modelName}/${id}`)
  }

  public edit(data, modelName: string): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(`/api/edit/${modelName}/${data.id}`, data);
  }

}
