import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { CalendarComponentComponent } from './calendar-component.component';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { Component } from '@angular/core';
import { MatSelectHarness } from '@angular/material/select/testing';


@Component({
  selector: 'daypilot-navigator',
  template: ''
})
export class MockDayPilotNavigatorComponent {}

@Component({
  selector: 'daypilot-calendar',
  template: ''
})
export class MockDayPilotCalendarComponent {}

fdescribe('CalendarComponentComponent', () => {
  let component: CalendarComponentComponent;
  let fixture: ComponentFixture<CalendarComponentComponent>;
  let loader: HarnessLoader;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CalendarComponentComponent,MockDayPilotNavigatorComponent,
        MockDayPilotCalendarComponent,],
      providers: [provideHttpClient(withInterceptorsFromDi()),
        provideAnimationsAsync(),
      ],
      declarations: [
        
        // other necessary imports
      ],
    })
      .compileComponents();

    fixture = TestBed.createComponent(CalendarComponentComponent);
    component = fixture.componentInstance;
    component.contractorNames = [{name: "alex", id: 1}]
    loader = TestbedHarnessEnvironment.loader(fixture);
    component.ngOnChanges();
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render correctly', () => {
    const compiled = fixture.debugElement.nativeElement;
    const navigator = compiled.querySelector('[data-testid="nav"]');
    const buttonsContainer = compiled.querySelector('[data-testid="buttons"]');
    const dayCalendar = compiled.querySelector('[data-testid="cal"]'); // First one
    const weekCalendar = compiled.querySelectorAll('[data-testid="cal"]')[1]; // Second one
    const select = loader.getHarness(MatSelectHarness)
    expect(navigator).toBeTruthy()
    expect(buttonsContainer).toBeTruthy()
    expect(dayCalendar).toBeTruthy()
    expect(weekCalendar).toBeTruthy()
    expect(select).toBeTruthy()
  })

  // it('should refetch on contractor change', () => {})

  // it('should create correctly', () => {})

  // it('should edit correctly', () => {})

  // it('should delete correctly', () => {})
});
