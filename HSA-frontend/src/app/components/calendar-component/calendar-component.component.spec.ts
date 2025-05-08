import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { CalendarComponentComponent } from './calendar-component.component';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { By } from '@angular/platform-browser';
import { DayPilot } from "@daypilot/daypilot-lite-angular";
import { of } from 'rxjs';

describe('CalendarComponentComponent', () => {
  let component: CalendarComponentComponent;
  let fixture: ComponentFixture<CalendarComponentComponent>;
  let loader: HarnessLoader;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CalendarComponentComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
      declarations: [],
    }).compileComponents();

    fixture = TestBed.createComponent(CalendarComponentComponent);
    component = fixture.componentInstance;
    component.contractorNames = [{ name: "alex", id: 1 }, { name: "alex1", id: 1 }];
    loader = TestbedHarnessEnvironment.loader(fixture);
    component.ngOnChanges();
    fixture.detectChanges();

    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('render correctly', () => {
    it('should have the all components', () => {
      const compiled = fixture.debugElement;
      expect(compiled.query(By.css('daypilot-navigator'))).toBeTruthy();
      expect(compiled.query(By.css('mat-select'))).toBeTruthy();
      expect(
        compiled
          .queryAll(By.css('button'))
          .some(b => b.nativeElement.textContent.trim() === 'Day')
      ).toBeTrue();
      expect(
        compiled
          .queryAll(By.css('button'))
          .some(b => b.nativeElement.textContent.trim() === 'Week')
      ).toBeTrue();
    });
  });

  // ———————————————
  // NEW TESTS START HERE
  // ———————————————

  it('viewDay()/viewWeek() toggle navigator and calendars', () => {
    component.viewDay();
    expect(component.configNavigator.selectMode).toBe('Day');
    expect(component.configDay.visible).toBeTrue();
    expect(component.configWeek.visible).toBeFalse();

    component.viewWeek();
    expect(component.configNavigator.selectMode).toBe('Week');
    expect(component.configDay.visible).toBeFalse();
    expect(component.configWeek.visible).toBeTrue();
  });

  it('eventHTML() returns formatted HTML', () => {
    const html = component.eventHTML('MyEvent', '05/06', 'CustName', 'TypeX');
    expect(html).toContain('<b>MyEvent</b>');
    expect(html).toContain('End: 05/06');
    expect(html).toContain('Customer: CustName');
    expect(html).toContain('Type: TypeX');
  });

  it('isDay() reflects configNavigator.selectMode', () => {
    component.configNavigator.selectMode = 'Day';
    expect(component.isDay()).toBeTrue();
    component.configNavigator.selectMode = 'Week';
    expect(component.isDay()).toBeFalse();
  });

  it('clearAllEvents() empties events and resets both calendars', () => {
    // stub day & week controls
    (component as any).day = { control: { events: { list: [1,2] }, update: jasmine.createSpy() } };
    (component as any).week = { control: { events: { list: [3] }, update: jasmine.createSpy() } };
    component.events = [{} as any, {} as any];

    component.clearAllEvents();

    expect(component.events.length).toBe(0);
    expect((component as any).day.control.events.list.length).toBe(0);
    expect((component as any).week.control.events.list.length).toBe(0);
    expect((component as any).day.control.update).toHaveBeenCalled();
    expect((component as any).week.control.update).toHaveBeenCalled();
  });

  it('changeDate() only fires on real date changes', () => {
    spyOn(component, 'clearAllEvents');
    spyOn(component, 'loadEvents');

    const today = component.date;
    component.staleDate = today; // same date: no-op
    component.changeDate(today);
    expect(component.clearAllEvents).not.toHaveBeenCalled();

    // now change to a new date
    const newDate = today.addDays(1);
    component.staleDate = today;
    component.changeDate(newDate);
    expect(component.clearAllEvents).toHaveBeenCalled();
    expect(component.loadEvents).toHaveBeenCalled();
    expect(component.staleDate).toBe(newDate);
    expect(component.configDay.startDate).toEqual(newDate);
    expect(component.configWeek.startDate).toEqual(newDate);
  });

  it('downloadIcal() calls createObjectURL and revokes it after click', () => {
    const blob = new Blob(['foo'], { type: 'text/calendar' });
    spyOn((component as any).calendarDataService, 'getIcal').and.returnValue(of(blob));
    const createSpy = spyOn(window.URL, 'createObjectURL').and.returnValue('blob:url');
    const revokeSpy = spyOn(window.URL, 'revokeObjectURL');
    const clickSpy = spyOn(HTMLAnchorElement.prototype, 'click');

    component.downloadIcal();

    expect(createSpy).toHaveBeenCalledWith(blob);
    expect(clickSpy).toHaveBeenCalled();
    expect(revokeSpy).toHaveBeenCalledWith('blob:url');
  });

  it('onBeforeEventRender() adds three areas (info, delete, default)', () => {
    // prepare a fake event and job
    component.jobs = [{ data: { id: 7, customerName: 'C', description: 'D' } }];
    const args: any = {
      control: {},
      data: { areas: [], tags: { jobID: 7, bookingType: 'B', status: 'S' }, text: 'E', backColor: '#fff' }
    };

    component.onBeforeEventRender(args);

    expect(args.data.areas.length).toBe(3);
    const info = args.data.areas.find((a: any) => a.toolTip === 'Info');
    const del  = args.data.areas.find((a: any) => a.toolTip === 'Delete event');
    const def  = args.data.areas.find((a: any) => a.bottom === 5 && a.left === 5);

    expect(info).toBeTruthy();
    expect(del).toBeTruthy();
    expect(def).toBeTruthy();
  });

  it('covers the job_data branch in loadEvents()', () => {
    // pretend the navigator exists so loadEvents() proceeds
    component.nav = {} as any;
    // stub getEvents to return one event + one job
    const today = DayPilot.Date.today().toString();
    spyOn((component as any).calendarDataService, 'getEvents').and.returnValue(of({
      event_data: [
        { id: 99, event_name: 'X', start_time: today, end_time: today,
          job: 1, booking_type: 'T', status: 'S', back_color: '#000' }
      ],
      job_data: [
        { data: { id: 1, endDate: '2025-05-06', customerName: 'Foo', description: 'Bar' } }
      ]
    }));
    // clear any prior state
    component.events = [];
    component.jobs = [];

    component.loadEvents();

    // branch ran, jobs[] got pushed and events[0].tags.jobDescription set
    expect(component.jobs.length).toBe(1);
    expect(component.events[0].tags.jobDescription).toBe('Bar');
  });

  it('covers onEventClick edit-flow branch', () => {
    // start with one job so the filter actually removes it
    component.jobs = [{ data: { id: 42 } }];

    // fake dialog result (truthy)
    const fakeResult = {
      tags: { jobID: 42, jobDescription: 'old', bookingType: 'B', status: 'S' },
      eventName: 'E',
      startTime: component.date.toString(),
      endTime: component.date.toString(),
      backColor: '#fff'
    };
    spyOn(component.dialog, 'open').and.returnValue({
      afterClosed: () => of(fakeResult)
    } as any);

    // fake jobService to return a new response
    const fakeResp = { data: { id: 42, endDate: '2025-05-06', customerName: 'Cust', description: 'NewDesc' } };
    spyOn((component as any).jobService, 'getSpecificJobData').and.returnValue(of(fakeResp));

    // minimal args with control.events.update spy
    const args: any = {
      e: { data: { tags: { jobID: 42 }, text: 'X', start: { value: '' }, end: { value: '' } } },
      control: { events: { update: jasmine.createSpy('update') } }
    };

    component.onEventClick(args);

    // after subscriptions, jobs[] should contain our fakeResp
    expect(component.jobs).toEqual([fakeResp]);
  });


  it('covers onTimeRangeSelected create-event branch', () => {
    // 1) Fake dialog.open → afterClosed() ⇒ our result
    const fakeResult = {
      tags: { jobID: 7, bookingType: 'BT', status: 'ST', jobDescription: 'JD' },
      eventName: 'Evt',
      startTime: DayPilot.Date.today().toString(),
      endTime:   DayPilot.Date.today().toString(),
      backColor: '#0F0'
    };
    (component as any).dialog = {
      open: () => ({ afterClosed: () => of(fakeResult) })
    };

    // 2) Stub jobService.getSpecificJobData
    const jobResp = {
      data: { id: 7, endDate: '2025-05-06', customerName: 'C', description: 'D' }
    };
    spyOn((component as any).jobService, 'getSpecificJobData').and.returnValue(of(jobResp));

    // 3) Stub calendarDataService.createEvent
    spyOn((component as any).calendarDataService, 'createEvent').and.returnValue(of({ data: { id: 99 } }));

    // 4) Replace snackBar with a fake that has open()
    (component as any).snackBar = { open: jasmine.createSpy('open') } as any;

    // 5) Fake DayPilot control
    const clearSpy = jasmine.createSpy('clearSelection');
    const addSpy   = jasmine.createSpy('add');
    const dp: any  = { clearSelection: clearSpy, events: { add: addSpy } };

    // 6) Invoke the handler under test
    component.onTimeRangeSelected({
      start:   { value: fakeResult.startTime },
      end:     { value: fakeResult.endTime },
      control: dp
    } as any);

    // 7) Assertions to drive coverage
    expect(clearSpy).toHaveBeenCalled();
    expect((component as any).jobService.getSpecificJobData).toHaveBeenCalledWith(7);
    expect((component as any).calendarDataService.createEvent).toHaveBeenCalled();
    expect((component as any).snackBar.open).toHaveBeenCalledWith('Event Created!', '', { duration: 3000 });
    expect(addSpy).toHaveBeenCalled();
    expect(component.jobs).toContain(jobResp);
  });

  it('covers delete-event callback in onBeforeEventRender with direct dialog/snackBar stub', () => {
    // start with two jobs—one should be filtered out
    component.jobs = [{ data: { id: 111 } }, { data: { id: 222 } }];

    // stub dialog.open → afterClosed() ⇒ true
    (component as any).dialog = {
      open: () => ({ afterClosed: () => of(true) })
    };

    // stub deleteEvent
    spyOn((component as any).calendarDataService, 'deleteEvent').and.returnValue(of({}));

    // replace snackBar with a fake
    (component as any).snackBar = { open: jasmine.createSpy('open') } as any;

    // fake DayPilot control
    const removeSpy = jasmine.createSpy('remove');
    const dp: any = { events: { remove: removeSpy } };

    // prepare the args
    const eventData = { id: 222, tags: { jobID: 222 }, text: 'X', backColor: '' };
    const args: any = { control: dp, data: eventData };

    // call to build areas[]
    component.onBeforeEventRender(args);

    // locate and invoke the delete-area click
    const delArea = args.data.areas.find((a: any) => a.toolTip === 'Delete event');
    delArea.onClick({ source: { data: eventData }, control: dp });

    // assertions to drive coverage
    expect((component as any).calendarDataService.deleteEvent).toHaveBeenCalledWith({ id: 222 });
    expect((component as any).snackBar.open).toHaveBeenCalledWith('Event Deleted!', '', { duration: 3000 });
    expect(removeSpy).toHaveBeenCalledWith({ data: eventData });
    // only the job matching jobID should remain
    expect(component.jobs).toEqual([{ data: { id: 222 } }]);
  });


});