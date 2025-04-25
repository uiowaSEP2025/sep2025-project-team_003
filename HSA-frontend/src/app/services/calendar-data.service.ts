import {Injectable} from "@angular/core";
import {Observable} from "rxjs";
import {DayPilot} from "@daypilot/daypilot-lite-angular";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {StandardApiResponse} from "../interfaces/api-responses/standard-api-response.interface";
import {BookingFetchResponse} from "../interfaces/api-responses/bookingJob.api.interface";

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



  // events = [
  //   {
  //     id: DayPilot.guid(),
  //     text: "Event 1",
  //     start: DayPilot.Date.today().firstDayOfWeek().addHours(10),
  //     end: DayPilot.Date.today().firstDayOfWeek().addHours(13),
  //     participants: 2,
  //     tags: {
  //       jobID: 1,
  //       jobDescription: "Hello",
  //       bookingType: "quote",
  //     },
  //     backColor: "#6aa84f"
  //   },
  //   {
  //     id: DayPilot.guid(),
  //     text: "Event 3",
  //     start: DayPilot.Date.today().addHours(10),
  //     end: DayPilot.Date.today().addHours(14),
  //     participants: 2,
  //     tags: {
  //       jobID: 3,
  //       jobDescription: "Hello",
  //       bookingType: "quote",
  //     },
  //     backColor: "#2e78d6"
  //   },
  // ];

  private apiGetUrl = `${environment.apiUrl}/api/get/bookings`;
  private apiCreateUrl = `${environment.apiUrl}/api/create/booking`;
  private apiEditUrl = `${environment.apiUrl}/api/edit/booking`;
  private apiDeleteUrl = `${environment.apiUrl}/api/delete/booking`;

  constructor(private http : HttpClient) {}

  public getEvents(from: DayPilot.Date, to: DayPilot.Date): Observable<BookingFetchResponse> {
    console.log(from,to)
    return this.http.get<BookingFetchResponse>(this.apiGetUrl + "?from=" + from.toString() + "&to=" + to.toString());
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

  getColors(): any[] {
    return [
      {name: "Green", id: BookingService.colors.green},
      {name: "Yellow", id: BookingService.colors.yellow},
      {name: "Red", id: BookingService.colors.red},
      {name: "Gray", id: BookingService.colors.gray},
      {name: "Blue", id: BookingService.colors.blue},
    ];
  }
}
