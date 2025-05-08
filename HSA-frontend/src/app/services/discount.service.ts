import { Injectable } from '@angular/core';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Customer, CustomerParams } from '../interfaces/customer.interface';
import { TableApiResponse } from '../interfaces/api-responses/table.api.interface';

interface getTableResponse {
    "id": number,
    "discount_name": string 
    "discount_percent": string 
}

interface createDiscountInterface {
    name:string | null,
    percent: string | null
}

interface editDiscountInterface {
  name:string | null,
  percent: string | null,
  id: string | null
}

@Injectable({
  providedIn: 'root'
})
export class DiscountsService {
  private apiGetUrl = `${environment.apiUrl}/api/get/discounts`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/discount`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/discount`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/discount`;

  constructor(private http: HttpClient) { }

  public getDiscounts(params?: Record<string, string | number>): Observable<TableApiResponse<getTableResponse>> {
    let httpParams = new HttpParams();

    // Add query parameters
    if (params) {
      Object.keys(params).forEach(key => {
        httpParams = httpParams.append(key, params[key])
      })
    }

    return this.http.get<TableApiResponse<getTableResponse>>(this.apiGetUrl, { params: httpParams });
  }

  public createDiscount(data: createDiscountInterface): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl, data);
  }

  public deleteDiscount(id: any) {
    id = id.id
    return this.http.post<StandardApiResponse>(`${this.apiDeleteUrl}/${id}`, null);
    
  }

  public editDiscount(data: editDiscountInterface) {
    return this.http.post<StandardApiResponse>(`${this.apiEditUrl}/${data.id}`, data);
  }
  
  
}
