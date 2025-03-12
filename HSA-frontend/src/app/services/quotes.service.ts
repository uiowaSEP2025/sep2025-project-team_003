import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { TableApiResponse } from '../interfaces/table.api.interface';
import { Quote } from '../interfaces/quote.interface';

@Injectable({
  providedIn: 'root'
})
export class MaterialService {
    private apiGetUrl = `${environment.apiUrl}/api/get/quotesforinvoice/customer/`

  constructor(private http: HttpClient) {}

  public getMaterial(id: number, params?: Record<string, string | number>): Observable<TableApiResponse<Quote>> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<TableApiResponse<Quote>>(`${this.apiGetUrl}/${id}`, { params: httpParams });
  }
}
