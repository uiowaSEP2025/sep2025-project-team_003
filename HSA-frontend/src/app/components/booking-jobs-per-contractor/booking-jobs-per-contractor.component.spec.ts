import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookingJobsPerContractorComponent } from './booking-jobs-per-contractor.component';

describe('BookingJobsPerContractorComponent', () => {
  let component: BookingJobsPerContractorComponent;
  let fixture: ComponentFixture<BookingJobsPerContractorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BookingJobsPerContractorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BookingJobsPerContractorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
