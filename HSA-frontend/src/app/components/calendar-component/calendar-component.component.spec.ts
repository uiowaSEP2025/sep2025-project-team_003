import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalendarComponentComponent } from './calendar-component.component';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

describe('CalendarComponentComponent', () => {
  let component: CalendarComponentComponent;
  let fixture: ComponentFixture<CalendarComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CalendarComponentComponent],
      providers: [provideHttpClient(withInterceptorsFromDi()),
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(CalendarComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
