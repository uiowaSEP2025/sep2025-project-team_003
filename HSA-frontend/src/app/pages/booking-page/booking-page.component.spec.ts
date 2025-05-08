import { ComponentFixture, TestBed } from '@angular/core/testing';
import { BookingDialogComponentComponent } from '../../components/booking-dialog-component/booking-dialog-component.component';
import { BookingPageComponent } from './booking-page.component';
import { HttpTestingController } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('BookingPageComponent', () => {
  let component: BookingPageComponent;
  let fixture: ComponentFixture<BookingPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        BookingPageComponent,
        MatDialogModule,  // Add MatDialogModule for dialog functionality
      ],
      providers: [
        provideHttpClient(withInterceptorsFromDi()),
        {
          provide: MatDialogRef,
          useValue: { close: jasmine.createSpy('close') }  // Mock MatDialogRef
        }
      ],
      schemas: [NO_ERRORS_SCHEMA]  // This can be used to ignore unrecognized elements (optional)
    })
    .compileComponents();

    fixture = TestBed.createComponent(BookingPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
