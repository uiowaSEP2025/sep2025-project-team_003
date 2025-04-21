import {FormsModule} from "@angular/forms";
import {NgModule} from "@angular/core";
import {DayPilotModule} from "@daypilot/daypilot-lite-angular";
import {provideHttpClient} from "@angular/common/http";
import {CommonModule} from "@angular/common";
import { DataService } from "../../services/calendar-data.service";

@NgModule({
  imports:      [
    CommonModule,
    FormsModule,
    DayPilotModule
  ],
  providers:    [
    DataService,
    provideHttpClient()
  ]
})
export class CalendarModule { }
