import {Injectable} from "@angular/core";
import {Observable} from "rxjs";
import {DayPilot} from "@daypilot/daypilot-lite-angular";
import {HttpClient} from "@angular/common/http";

@Injectable({
    providedIn: 'root'
})
export class DataService {

  static colors = {
    green: "#6aa84f",
    yellow: "#f1c232",
    red: "#cc4125",
    gray: "#808080",
    blue: "#2e78d6",
  };

  exampleDate = "01/02"
  exampleCustomer = "John Doe"

  events = [
    {
      id: DayPilot.guid(),
      text: "Event 1",
      start: DayPilot.Date.today().firstDayOfWeek().addHours(10),
      end: DayPilot.Date.today().firstDayOfWeek().addHours(13),
      participants: 2,
      tags: {
        jobID: "1",
        jobDescription: "Hello",
        bookingType: "quote",
      },
      backColor: "#6aa84f"
    },
    {
      id: DayPilot.guid(),
      text: "Event 3",
      start: DayPilot.Date.today().addHours(10),
      end: DayPilot.Date.today().addHours(14),
      participants: 2,
      tags: {
        jobID: "3",
        jobDescription: "Hello",
        bookingType: "quote",
      },
      backColor: "#2e78d6"
    },
  ];

  constructor(private http : HttpClient){
  }

  getEvents(from: DayPilot.Date, to: DayPilot.Date): Observable<any[]> {

    // simulating an HTTP request
    return new Observable(observer => {
      setTimeout(() => {
        observer.next(this.events);
      }, 200);
    });

    // return this.http.get("/api/events?from=" + from.toString() + "&to=" + to.toString());
  }

  getColors(): any[] {
      const colors = [
        {name: "Green", id: DataService.colors.green},
        {name: "Yellow", id: DataService.colors.yellow},
        {name: "Red", id: DataService.colors.red},
        {name: "Gray", id: DataService.colors.gray},
        {name: "Blue", id: DataService.colors.blue},
      ];
      return colors;
  }

}
