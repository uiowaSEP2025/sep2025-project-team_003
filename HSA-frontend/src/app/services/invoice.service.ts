import { Injectable } from "@angular/core";
import { environment } from "../../environments/environment";
import { HttpClient } from "@angular/common/http";
import { TableApiResponse } from "../interfaces/api-responses/table.api.interface";
import { Invoice } from "../interfaces/invoice.interface";
import { Observable } from "rxjs";
import { HttpParams } from "@angular/common/http";
import { StandardApiResponse } from "../interfaces/api-responses/standard-api-response.interface";
import { InvoiceDataInterface } from "../interfaces/api-responses/invoice.api.data.interface";

interface CreateInvoiceInterface {
    customerID: number,
    quoteIDs: number[]
}

@Injectable({
    providedIn: 'root'
})
export class InvoiceService {
    private apiGetUrl = `${environment.apiUrl}/api/get/invoices`;
    private createUrl = `${environment.apiUrl}/api/create/invoice`;
    private getSpecificUrl = `${environment.apiUrl}/api/get/invoice/displaydata`;

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

    public createInvoice(json: CreateInvoiceInterface): Observable<StandardApiResponse> {
        return this.http.post<StandardApiResponse>(this.createUrl, json);
    }

    public getSpecificInvoiceData(id: number): Observable<InvoiceDataInterface> {
        return this.http.get<InvoiceDataInterface>(`${this.getSpecificUrl}/${id}`);
    }

}
