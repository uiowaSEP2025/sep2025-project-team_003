import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { DayPilot, DayPilotCalendarComponent, DayPilotModule, DayPilotNavigatorComponent } from "@daypilot/daypilot-lite-angular";
import { DataService } from '../../services/calendar-data.service';
import { MatDialog } from '@angular/material/dialog';
import { BookingDialogComponentComponent } from '../booking-dialog-component/booking-dialog-component.component';
import { DeleteDialogComponentComponent } from '../delete-dialog-component/delete-dialog-component.component';
import { JobService } from '../../services/job.service';
import { ViewJobDialogComponentComponent } from '../view-job-dialog-component/view-job-dialog-component.component';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-calendar-component',
  imports: [
    DayPilotModule,
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
  jobs: any[] = [];
  date = DayPilot.Date.today();

  configNavigator: DayPilot.NavigatorConfig = {
    showMonths: 3,
    cellWidth: 25,
    cellHeight: 25,
    onVisibleRangeChanged: args => {
      this.loadEvents();
    }
  };

  changeDate(date: DayPilot.Date): void {
    this.configDay.startDate = date;
    this.configWeek.startDate = date;
  }

  configDay: DayPilot.CalendarConfig = {
    durationBarVisible: false,
    onTimeRangeSelected: this.onTimeRangeSelected.bind(this),
    onBeforeEventRender: this.onBeforeEventRender.bind(this),
    onEventClick: this.onEventClick.bind(this),
    
    //handling drag event
    eventMoveHandling: "Update",
    onEventMove: (args) => { 
      this.onChangeViaDragAndResize(args)
    },

    //handling resize event
    eventResizeHandling: "Update",
    onEventResize: (args) => {
      this.onChangeViaDragAndResize(args)
    }
  };

  configWeek: DayPilot.CalendarConfig = {
    viewType: "Week",
    durationBarVisible: false,
    onTimeRangeSelected: this.onTimeRangeSelected.bind(this),
    onBeforeEventRender: this.onBeforeEventRender.bind(this),
    onEventClick: this.onEventClick.bind(this),

    //handling drag event
    eventMoveHandling: "Update",
    onEventMove: (args) => { 
      this.onChangeViaDragAndResize(args)
    },

    //handling resize event
    eventResizeHandling: "Update",
    onEventResize: (args) => {
      this.onChangeViaDragAndResize(args)
    }
  };

  constructor(
    private calendarDataService: DataService, 
    private jobService: JobService, 
    public dialog: MatDialog, 
    private snackBar: MatSnackBar
  ) {
    this.viewWeek();
  }

  ngAfterViewInit(): void {
    this.loadEvents();
  }

  eventHTML(eventName: string, endDate: string, customerName: string, typeOfEvent: string) {
    return `<div style="margin-top: 20px;">
              <b>${eventName}</b>
              <br> 
              <b style='color:#9e1414;'>End: ${endDate}</b>
              <br>
              <b>Customer: ${customerName}</b>
              <br>
              <b>Type: ${typeOfEvent}</b>
            </div>`
  }

  loadEvents(): void {
    const from = this.nav.control.visibleStart();
    const to = this.nav.control.visibleEnd();

    //load events from booking model
    this.calendarDataService.getEvents(from, to).subscribe({
      next: (response) => {
        let allEvents: any = response
        
        if (allEvents.data.length !== 0) {
          //load job data for each event (Or made an aggregate api to do this once)
          allEvents.data.forEach((element: any) => {
            let eventFormat = new DayPilot.Event({
              id: element.id,
              text: element["event_name"],
              start: new DayPilot.Date(element["start_time"], true),
              end: new DayPilot.Date(element["end_time"], true),
              tags: {
                jobID: element["job"],
                bookingType: element["booking_type"],
                status: element["status"]
              },
              backColor: element["back_color"]
            })

            this.jobService.getSpecificJobData(eventFormat.data.tags.jobID).subscribe({
              next: (response) => {
                this.jobs.push(response)
                let endDate = response.data.endDate.split("-").slice(1).join("/");
                eventFormat.data.html = this.eventHTML(eventFormat.data.text, endDate, response.data.customerName, eventFormat.data.tags.bookingType)
                eventFormat.data.tags.jobDescription = response.data.description

                this.events.push(eventFormat.data)
              }
            });
            
          });
        }
      }
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
        right: 25,
        width: 20,
        height: 20,
        symbol: "/icons/daypilot.svg#i-circle",
        fontColor: "#000",
        action: "None",
        toolTip: "Info",
        onClick: async (args: any)  => {
          const infoData = {
            jobInfo: this.jobs.filter((item) => item.data.id === args.source.data.tags.jobID)[0],
            bookingInfo: {
              eventName: args.source.data.text,
              status: args.source.data.tags.status,
              bookingType: args.source.data.tags.bookingType
            }
          };

          const dialogRef = this.dialog.open(ViewJobDialogComponentComponent, {
            width: 'auto', 
            maxWidth: '90vw', 
            height: 'auto', 
            maxHeight: '90vh',
            data: infoData
          });
      
          dialogRef.afterClosed().subscribe(result => {});
        }
      },
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
            id: args.source.data.id,
            eventName: args.source.data.text
          }

          const dialogRef = this.dialog.open(DeleteDialogComponentComponent, {
            width: '425px',
            data: messageData
          });

          
      
          dialogRef.afterClosed().subscribe(result => {
            if (result) {
              //call the api to delete booking model here
              this.calendarDataService.deleteEvent({ id: args.source.data.id}).subscribe({
                next: (response) => {
                  this.snackBar.open('Event Deleted!', '', {
                    duration: 3000
                  });

                  dp.events.remove(args.source);
                  this.jobs = this.jobs.filter((item) => item.data.id === args.source.data.tags.jobID)
                },
                error: (error) => {}
            })
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
    console.log(typeof args.end.value)
    const slotData = {
      startTime: args.start.value,
      endTime: args.end.value,
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
      const dp = args.control;
      dp.clearSelection(); // clears the highlighting that the user used to create the event
      if (result) {
        this.jobService.getSpecificJobData(result.tags.jobID).subscribe({ // to take the job info
          next: (response) => {
            this.jobs.push(response)
            let jobInfo = response.data

            const endDate = jobInfo["endDate"].split("-").slice(1).join("/");

            dp.events.add(new DayPilot.Event({
              start: new DayPilot.Date(result.startTime, true),
              end: new DayPilot.Date(result.endTime, true),
              html: this.eventHTML(result.eventName, endDate, jobInfo['customerName'], result.bookingType),
              id: DayPilot.guid(),
              text: result.eventName,
              backColor: result.backColor,
              tags: {
                jobID: result.tags.jobID,
                jobDescription: result.tags.jobDescription,
                bookingType: result.tags.bookingType,
                status: result.tags.status
              }
            }));
            
            const eventCreateRequest = {
              eventName: result.eventName,
              startTime: new DayPilot.Date(result.startTime, true).toString(),
              endTime: new DayPilot.Date(result.endTime, true).toString(),
              bookingType: result.tags.bookingType,
              backColor: result.backColor,
              status: result.tags.status,
              jobID: result.tags.jobID
            }

            //call the api to save booking model here
            this.calendarDataService.createEvent(eventCreateRequest).subscribe({
              next: (response) => {
                this.snackBar.open('Event Created!', '', {
                  duration: 3000
                });
              },
              error: (error) => {}
            })
          }
        })
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
      status: args.e.data.tags.status,
      backColor: args.e.data.backColor,
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
        this.jobs = this.jobs.filter((item) => item.data.id !== args.e.data.tags.jobID) 
        
        this.jobService.getSpecificJobData(result.tags.jobID).subscribe({
          next: (response) => {
            this.jobs.push(response)
            let jobInfo = response.data

            const endDate = jobInfo["endDate"].split("-").slice(1).join("/");
        
            const updateEventData = new DayPilot.Event({
              id: args.e.data.id,
              text: result.eventName,
              html: this.eventHTML(result.eventName, endDate, jobInfo['customerName'], result.tags.bookingType),
              start: new DayPilot.Date(result.startTime, true),
              end: new DayPilot.Date(result.endTime, true),
              tags: {
                jobID: result.tags.jobID,
                jobDescription: result.tags.jobDescription,
                bookingType: result.tags.bookingType,
                status: result.tags.status,
              },
              backColor: result.backColor
            });

            dp.events.update(updateEventData.data)

            const eventEditRequest = {
              id: args.e.data.id,
              eventName: result.eventName,
              startTime: new DayPilot.Date(result.startTime, true).toString(),
              endTime: new DayPilot.Date(result.endTime, true).toString(),
              bookingType: result.tags.bookingType,
              backColor: result.backColor,
              status: result.tags.status,
              jobID: result.tags.jobID
            }

            //call the api to save booking model here
            this.calendarDataService.editEvent(eventEditRequest).subscribe({
              next: (response) => {
                this.snackBar.open('Event Edited!', '', {
                  duration: 3000
                });
              },
              error: (error) => {}
            })
          }
        })
      }
    });
  }

  onChangeViaDragAndResize(args: any) {
    const eventEditRequest = {
      id: args.e.data.id,
      eventName: args.e.data.text,
      startTime: new DayPilot.Date(args.newStart, true).toString(),
      endTime: new DayPilot.Date(args.newEnd, true).toString(),
      bookingType: args.e.data.tags.bookingType,
      backColor: args.e.data.backColor,
      status: args.e.data.tags.status,
      jobID: args.e.data.tags.jobID
    }

    this.calendarDataService.editEvent(eventEditRequest).subscribe({
      next: (response) => {
        this.snackBar.open('Event Edited!', '', {
          duration: 3000
        });
      },
      error: (error) => {}
    })
  }
}
