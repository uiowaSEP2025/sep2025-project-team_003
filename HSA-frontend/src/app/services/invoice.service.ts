import { Injectable } from "@angular/core";
import { environment } from "../../environments/environment";
import { HttpClient } from "@angular/common/http";
import { TableApiResponse } from "../interfaces/api-responses/table.api.interface";
import { Observable } from "rxjs";
import { Invoice } from "../components/invoice-job/invoice-job.component";
import { HttpParams } from "@angular/common/http";
import { StandardApiResponse } from "../interfaces/api-responses/standard-api-response.interface";

interface CreateInvoiceInterface {
    customerID: number,
    jobIds: number[],
    status: "created" | "issued" | "paid"
    issuedDate: string,
    dueDate: string,
    tax: string
}

interface UpdateInvoiceInterface {
        jobIds: number[],
        status: "created" | "issued" | "paid",
        issuedDate: string,
        dueDate: string, 
        tax: string,
        url: string | null
}

@Injectable({
    providedIn: 'root'
})
export class InvoiceService {
    private apiGetUrl = `${environment.apiUrl}/api/get/invoices`;
    private createUrl = `${environment.apiUrl}/api/create/invoice`;
    private deleteUrl = `${environment.apiUrl}/api/delete/invoice`;
    private getSpecificUrl = `${environment.apiUrl}/api/get/invoice/displaydata`;
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
        return this.http.post<StandardApiResponse>(this.createUrl, json);
    }

    public updateInvoice(id: number, data: UpdateInvoiceInterface) {
        return this.http.post<StandardApiResponse>(`${this.editUrl}/${id}`, data);
    }

    public deleteInvoice(row: any): Observable<StandardApiResponse> {
        const id = row.id
        return this.http.post<StandardApiResponse>(`${this.deleteUrl}/${id}`, null);
    }

    public getSpecificInvoiceData(id: number): Observable<Invoice> {
        return this.http.get<Invoice>(`${this.getSpecificUrl}/${id}`);
    }

}
