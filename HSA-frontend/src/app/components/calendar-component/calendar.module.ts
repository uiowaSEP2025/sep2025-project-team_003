import {FormsModule} from "@angular/forms";
import {NgModule} from "@angular/core";
import {DayPilotModule} from "@daypilot/daypilot-lite-angular";
import {provideHttpClient} from "@angular/common/http";
import {CommonModule} from "@angular/common";

@NgModule({
  imports:      [
    CommonModule,
    FormsModule,
    DayPilotModule
  ],
  providers:    [
    provideHttpClient()
  ]
})
export class CalendarModule { }
