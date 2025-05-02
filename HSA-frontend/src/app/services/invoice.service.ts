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
    quoteIDs: number[],
    status: "created" | "issued" | "paid"
    dateIssued: string,
    dateDue: string,
    taxPercent: string
}

interface UpdateInvoiceInterface {
        quoteIDs: number[],
        status: "created" | "issued" | "paid",
        dateIssued: string,
        dateDue: string,
        taxPercent: string
}

@Injectable({
    providedIn: 'root'
})
export class InvoiceService {
    private apiGetUrl = `${environment.apiUrl}/api/get/invoices`;
    private createUrl = `${environment.apiUrl}/api/create/invoice`;
    private deleteUrl = `${environment.apiUrl}/api/delete/invoice`;
    private getSpecificUrl = `${environment.apiUrl}/api/get/invoice/`;
    private editUrl = `${environment.apiUrl}/api/edit/invoice`;


    private convertTaxInputToMathPercent(input: string): string {
        if (input === "100") {
            return "1.00"
        }
        return input.length === 2 ? `0.${input}` : `0.0${input}`
    }

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
        json.taxPercent = this.convertTaxInputToMathPercent(json.taxPercent)
        return this.http.post<StandardApiResponse>(this.createUrl, json);
    }

    public updateInvoice(id: number, data: UpdateInvoiceInterface) {
        data.taxPercent = this.convertTaxInputToMathPercent(data.taxPercent)
        return this.http.post<StandardApiResponse>(`${this.editUrl}/${id}`, data);
    }

    public deleteInvoice(row: any): Observable<StandardApiResponse> {
        const id = row.id
        return this.http.post<StandardApiResponse>(`${this.deleteUrl}/${id}`, null);
    }

    public getSpecificInvoiceData(id: number): Observable<InvoiceDataInterface> {
        return this.http.get<InvoiceDataInterface>(`${this.getSpecificUrl}/${id}`);
    }

}
