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
export class InvoiceService {
    private apiGetUrl = `${environment.apiUrl}/ `;

    constructor(private http: HttpClient) { }

    public getInvoicesForOrganization(params?: Record<string, string | number>): Observable<TableApiResponse<Invoice>> {
        let httpParams = new HttpParams();

        // Add query parameters
        if (params) {
            Object.keys(params).forEach(key => {
                httpParams = httpParams.append(key, params[key])
            })
        }

        return this.http.get<TableApiResponse<Invoice>>(this.apiGetUrl, { params: httpParams });
    }

}
