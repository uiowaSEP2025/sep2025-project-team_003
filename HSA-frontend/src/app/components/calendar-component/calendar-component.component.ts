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

  contextMenu = new DayPilot.Menu({
    items: [
      {
        text: "Edit",
        onClick: async args => {
          const event = args.source;
          const dp = event.calendar;

          const modal = await DayPilot.Modal.prompt("Edit event text:", event.data.text);
          dp.clearSelection();

          console.log(modal.result)
          if (!modal.result) { 
            return; 
          }

          event.data.text = modal.result;
          dp.events.update(event);
        }
      },
      {
        text: "Delete",
        onClick: args => {
          const event = args.source;
          const dp = event.calendar;
          dp.events.remove(event);
        }
      },
      
    ]
  });

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
    contextMenu: this.contextMenu,
    onTimeRangeSelected: this.onTimeRangeSelected.bind(this),
    onBeforeEventRender: this.onBeforeEventRender.bind(this),
    onEventClick: this.onEventClick.bind(this),
  };

  configWeek: DayPilot.CalendarConfig = {
    viewType: "Week",
    durationBarVisible: false,
    contextMenu: this.contextMenu,
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
        symbol: "/icons/daypilot.svg#minichevron-down-2",
        fontColor: "#fff",
        toolTip: "Show context menu",
        action: "ContextMenu",
      },
      {
        top: 3,
        right: 25,
        width: 20,
        height: 20,
        symbol: "/icons/daypilot.svg#x-circle",
        fontColor: "#fff",
        action: "None",
        toolTip: "Delete event",
        onClick: async (args: any)   => {
          dp.events.remove(args.source);
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
      listOfColor: this.calendarDataService.getColors()
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

        console.log(result)

        dp.events.add(new DayPilot.Event({
          start: new DayPilot.Date(result.startTime, true),
          end: new DayPilot.Date(result.endTime, true),
          id: DayPilot.guid(),
          text: result.eventName,
          backColor: result.color.id
        }));
      }
    });
  }

  async onEventClick(args: any) {
    const form = [
      {name: "Text", id: "text"},
      {name: "Start", id: "start", dateFormat: "MM/dd/yyyy", type: "datetime"},
      {name: "End", id: "end", dateFormat: "MM/dd/yyyy", type: "datetime"},
      {name: "Color", id: "backColor", type: "select", options: this.calendarDataService.getColors()},
    ];

    const data = args.e.data;
    console.log(args.e.data)

    const modal = await DayPilot.Modal.form(form, data);

    console.log(modal.result)

    if (modal.canceled) {
      return;
    }

    const dp = args.control;

    dp.events.update(modal.result);
  }

}
