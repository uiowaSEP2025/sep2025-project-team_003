import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { CalendarComponentComponent } from './calendar-component.component';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { Component } from '@angular/core';
import { MatSelectHarness } from '@angular/material/select/testing';
import { By } from '@angular/platform-browser';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';

fdescribe('CalendarComponentComponent', () => {
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
    })
      .compileComponents();

    fixture = TestBed.createComponent(CalendarComponentComponent);
    component = fixture.componentInstance;
    component.contractorNames = [{ name: "alex", id: 1 }, { name: "alex1", id: 1 }];
    loader = TestbedHarnessEnvironment.loader(fixture);
    component.loadEvents = () => { };
    component.ngOnChanges();
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('render correctly', () => {
    it('should have the all components', () => {
      const compiled = fixture.debugElement
      const navigatorElement = compiled.query(By.css('daypilot-navigator'));
      expect(navigatorElement).toBeTruthy();

      const matSelectElement = compiled.query(By.css('mat-select'));
      expect(matSelectElement).toBeTruthy();

      const dayButton = compiled.queryAll(By.css('button'))
        .find(button => button.nativeElement.textContent.trim() === 'Day');
      expect(dayButton).toBeTruthy();

      const weekButton = compiled.queryAll(By.css('button'))
        .find(button => button.nativeElement.textContent.trim() === 'Week');
      expect(weekButton).toBeTruthy();
    })

    it('should have the correct contractors in the select', () => {

    })
  })

  it('refetch on contractor change', () => { })


});
