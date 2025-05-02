import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookingDialogComponentComponent } from './booking-dialog-component.component';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

describe('BookingDialogComponentComponent', () => {
  let component: BookingDialogComponentComponent;
  let fixture: ComponentFixture<BookingDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        BookingDialogComponentComponent,
        MatDialogModule,
      ],
      providers: [
        provideAnimationsAsync(),
        {
          provide: MatDialogRef,
          useValue: { close: jasmine.createSpy('close') }
        },
        {
          provide: MAT_DIALOG_DATA,
          useValue: { eventName: '', bookingType: '', jobID:2, jobDescription:"", status:"complete", backColor:"blue" }
        }
      ],
      schemas: [NO_ERRORS_SCHEMA]  
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
