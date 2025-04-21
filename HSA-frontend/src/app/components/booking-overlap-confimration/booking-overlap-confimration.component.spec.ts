import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookingOverlapConfimrationComponent } from './booking-overlap-confimration.component';

describe('BookingOverlapConfimrationComponent', () => {
  let component: BookingOverlapConfimrationComponent;
  let fixture: ComponentFixture<BookingOverlapConfimrationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BookingOverlapConfimrationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BookingOverlapConfimrationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
