import { AfterViewInit, Component, ViewChild } from '@angular/core';
import {
  DayPilot,
  DayPilotCalendarComponent,
  DayPilotModule,
  DayPilotNavigatorComponent
} from "@daypilot/daypilot-lite-angular";
import { DataService } from '../../services/calendar-data.service';
import { MatDialog } from '@angular/material/dialog';
import { BookingDialogComponentComponent } from '../booking-dialog-component/booking-dialog-component.component';
import { DeleteDialogComponentComponent } from '../delete-dialog-component/delete-dialog-component.component';

@Component({
  selector: 'app-calendar-component',
  imports: [
    DayPilotModule
  ],
  providers:    [
    DataService,
  ],
  templateUrl: './calendar-component.component.html',
  styleUrl: './calendar-component.component.scss'
})
export class CalendarComponentComponent implements AfterViewInit {
  @ViewChild("day") day!: DayPilotCalendarComponent;
  @ViewChild("week") week!: DayPilotCalendarComponent;
  @ViewChild("navigator") nav!: DayPilotNavigatorComponent;

  events: DayPilot.EventData[] = [];
  date = DayPilot.Date.today();

  configNavigator: DayPilot.NavigatorConfig = {
    showMonths: 3,
    cellWidth: 25,
    cellHeight: 25,
    onVisibleRangeChanged: args => {
      this.loadEvents();
    }
  };

  selectTomorrow() {
    this.date = DayPilot.Date.today().addDays(1);
  }

  changeDate(date: DayPilot.Date): void {
    this.configDay.startDate = date;
    this.configWeek.startDate = date;
  }

  configDay: DayPilot.CalendarConfig = {
    durationBarVisible: false,
    onTimeRangeSelected: this.onTimeRangeSelected.bind(this),
    onBeforeEventRender: this.onBeforeEventRender.bind(this),
    onEventClick: this.onEventClick.bind(this),
  };

  configWeek: DayPilot.CalendarConfig = {
    viewType: "Week",
    durationBarVisible: false,
    onTimeRangeSelected: this.onTimeRangeSelected.bind(this),
    onBeforeEventRender: this.onBeforeEventRender.bind(this),
    onEventClick: this.onEventClick.bind(this),
  };

  constructor(private calendarDataService: DataService, public dialog: MatDialog) {
    this.viewWeek();
  }

  ngAfterViewInit(): void {
    this.loadEvents();
  }

  loadEvents(): void {
    const from = this.nav.control.visibleStart();
    const to = this.nav.control.visibleEnd();
    this.calendarDataService.getEvents(from, to).subscribe(result => {
      this.events = result;
    });
  }

  viewDay():void {
    this.configNavigator.selectMode = "Day";
    this.configDay.visible = true;
    this.configWeek.visible = false;
  }

  viewWeek():void {
    this.configNavigator.selectMode = "Week";
    this.configDay.visible = false;
    this.configWeek.visible = true;
  }

  onBeforeEventRender(args: any) {
    const dp = args.control;
    args.data.areas = [
      {
        top: 3,
        right: 3,
        width: 20,
        height: 20,
        symbol: "/icons/daypilot.svg#x-circle",
        fontColor: "#000",
        action: "None",
        toolTip: "Delete event",
        onClick: async (args: any)  => {
          const messageData = {
            id: args.source.cache.id,
            eventName: args.source.cache.text
          }

          const dialogRef = this.dialog.open(DeleteDialogComponentComponent, {
            width: '425px',
            data: messageData
          });
      
          dialogRef.afterClosed().subscribe(result => {
            if (result) {
              dp.events.remove(args.source);
            }
          });
        }
      }
    ];

    args.data.areas.push({
      bottom: 5,
      left: 5,
      width: 36,
      height: 36,
      action: "None",
    });
  }

  async onTimeRangeSelected(args: any) {
    const slotData = {
      startTime: args.start.value,
      listOfColor: this.calendarDataService.getColors(),
      typeOfDialog: "create"
    }

    const dialogRef = this.dialog.open(BookingDialogComponentComponent, {
      width: '800px', 
      maxWidth: '90vw', 
      height: 'auto', 
      maxHeight: '90vh',
      data: slotData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        const dp = args.control;
        dp.clearSelection();

        dp.events.add(new DayPilot.Event({
          start: new DayPilot.Date(result.startTime, true),
          end: new DayPilot.Date(result.endTime, true),
          id: DayPilot.guid(),
          text: result.eventName,
          backColor: result.backColor,
          tags: {
            jobID: result.tags.jobID,
            jobDescription: result.tags.jobDescription,
            bookingType: result.tags.bookingType
          }
        }));
      }
    });
  }

  async onEventClick(args: any) {
    const currentEventData = {
      eventName: args.e.data.text,
      startTime: args.e.data.start.value,
      endTime: args.e.data.end.value,
      jobID: args.e.data.tags.jobID,
      jobDescription: args.e.data.tags.jobDescription,
      bookingType: args.e.data.tags.bookingType,
      listOfColor: this.calendarDataService.getColors(),
      typeOfDialog: "edit",
      backColor: args.e.data.backColor
    }

    const dialogRef = this.dialog.open(BookingDialogComponentComponent, {
      width: '800px', 
      maxWidth: '90vw', 
      height: 'auto', 
      maxHeight: '90vh',
      data: currentEventData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        const dp = args.control

        const updateEventData = new DayPilot.Event({
          id: args.e.data.id,
          text: result.eventName,
          start: new DayPilot.Date(result.startTime, true),
          end: new DayPilot.Date(result.endTime, true),
          tags: {
            jobID: result.tags.jobID,
            jobDescription: result.tags.jobDescription,
            bookingType: result.tags.bookingType
          },
          backColor: result.backColor
        });

        console.log(updateEventData.data)

        dp.events.update(updateEventData.data)
      }
    });
  }

  openDeleteDialog(args: any) {
    
  }
}
