import {Injectable} from "@angular/core";
import {Observable} from "rxjs";
import {DayPilot} from "@daypilot/daypilot-lite-angular";
import {HttpClient, HttpParams} from "@angular/common/http";
import { environment } from "../../environments/environment";
import { StandardApiResponse } from "../interfaces/api-responses/standard-api-response.interface";
import { BookingFetchResponse } from "../interfaces/api-responses/bookingJob.api.interface";

interface BookingCreatePostData {
  eventName: string | null
  startTime: string | null
  endTime: string | null
  bookingType: string | null
  backColor: string | null
  status: string | null
  jobID: number | null
}

interface BookingEditPostData {
  id: number | null
  eventName: string | null
  startTime: string | null
  endTime: string | null
  bookingType: string | null
  backColor: string | null
  status: string | null
  jobID: number | null
}

interface BookingDeletePostData {
  id: number | null
}

@Injectable({
    providedIn: 'root'
})
export class BookingService {
  static colors = {
    green: "#6aa84f",
    yellow: "#f1c232",
    red: "#cc4125",
    gray: "#808080",
    blue: "#2e78d6",
  };

  private apiGetUrl = `${environment.apiUrl}/api/get/bookings`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/booking`;
  private apiIcalUrl = `${environment.apiUrl}/api/icals/booking`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/booking`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/booking`;

  constructor(private http : HttpClient) {}


  public getEvents(from: DayPilot.Date, to: DayPilot.Date, contractorId: number): Observable<BookingFetchResponse> {
    return this.http.get<BookingFetchResponse>(this.apiGetUrl + "?from=" + from.toString() + "&to=" + to.toString() + "&contractor=" + contractorId);
  }

  public createEvent(data: BookingCreatePostData): Observable<any> {
    return this.http.post<StandardApiResponse>(this.apiCreateUrl, data)
  }

  public editEvent(data: BookingEditPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiEditUrl + `/${data.id}`, data)
  }

  public deleteEvent(data: BookingDeletePostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiDeleteUrl + `/${data.id}`, data)
  }

  public getIcal(from: DayPilot.Date, to:DayPilot.Date, contractorId: number) {
    const url = `${this.apiIcalUrl}?from=${from}&to=${to}&contractor=${contractorId}`;
    return this.http.get(url, { responseType: 'blob' as 'blob' });
  }

  getColors(): any[] {
    const colors = [
      {name: "Green", id: BookingService.colors.green},
      {name: "Yellow", id: BookingService.colors.yellow},
      {name: "Red", id: BookingService.colors.red},
      {name: "Gray", id: BookingService.colors.gray},
      {name: "Blue", id: BookingService.colors.blue},
    ];
    return colors;
  }
}
