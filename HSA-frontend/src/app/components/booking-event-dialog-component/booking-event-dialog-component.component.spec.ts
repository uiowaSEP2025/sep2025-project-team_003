import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookingEventDialogComponentComponent } from './booking-event-dialog-component.component';

describe('BookingEventDialogComponentComponent', () => {
  let component: BookingEventDialogComponentComponent;
  let fixture: ComponentFixture<BookingEventDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BookingEventDialogComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BookingEventDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
