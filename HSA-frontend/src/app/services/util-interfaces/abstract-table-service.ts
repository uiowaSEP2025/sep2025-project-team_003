import { Observable } from "rxjs";
import { TableApiResponse } from "../../interfaces/api-responses/table.api.interface";

export abstract class AbstractTableService {
    // Abstract method (does not have a body)
    abstract fetchTable(search: string, pageOffset: string, pageSize: number): Observable<TableApiResponse<any>>;
}
