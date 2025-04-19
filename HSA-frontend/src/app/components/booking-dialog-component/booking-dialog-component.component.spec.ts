import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookingDialogComponentComponent } from './booking-dialog-component.component';

describe('BookingDialogComponentComponent', () => {
  let component: BookingDialogComponentComponent;
  let fixture: ComponentFixture<BookingDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BookingDialogComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BookingDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
