import { Injectable } from "@angular/core";
import { environment } from "../../environments/environment";
import { HttpClient } from "@angular/common/http";
import { TableApiResponse } from "../interfaces/table.api.interface";
import { Invoice } from "../interfaces/invoice.interface";
import { Observable } from "rxjs";
import { HttpParams } from "@angular/common/http";

@Injectable({
    providedIn: 'root'
})
export class QuoteService {
    private apiGetByCustomerUrl = `${environment.apiUrl}/api/get/quotesforinvoice/customer`;

    constructor(private http: HttpClient) { }

    public getQuotesByCustomer(id: number, params?: Record<string, string | number>): Observable<TableApiResponse<Invoice>> {
        let httpParams = new HttpParams();

        // Add query parameters
        if (params) {
            Object.keys(params).forEach(key => {
                httpParams = httpParams.append(key, params[key])
            })
        }
        console.log(`endpoint is ${this.apiGetByCustomerUrl}/${id}`)
        console.log(`got params: ${JSON.stringify(params)}`)
        return this.http.get<TableApiResponse<Invoice>>(`${this.apiGetByCustomerUrl}/${id}`, { params: httpParams });
    }

}
