import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewJobDialogComponentComponent } from './view-job-dialog-component.component';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';

// Mock MatDialogRef
class MatDialogRefMock {
  close() { }
}

describe('ViewJobDialogComponentComponent', () => {
  let component: ViewJobDialogComponentComponent;
  let fixture: ComponentFixture<ViewJobDialogComponentComponent>;


  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        MatDialogModule,
      ],
      providers: [
        { provide: MatDialogRef, useClass: MatDialogRefMock },
        {
          provide: MAT_DIALOG_DATA,
          useValue: {
            "jobInfo": {
              "data": {
                "customerName": "John Doe",
                "jobStatus": "In Progress",
                "startDate": "2025-04-15",
                "endDate": "2025-04-20",
                "description": "Electrical work for residential home",
                "requestorAddress": "123 Main St",
                "requestorCity": "Springfield",
                "requestorState": "IL",
                "requestorZip": "62701",
                "id": "JOB123456"
              }
            },
            bookingInfo: { /* mock your bookingInfo data here */ }
          }
        }
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ViewJobDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render job and booking information when jobData is present', () => {
    const fixture = TestBed.createComponent(ViewJobDialogComponentComponent);
    fixture.detectChanges();
  
    const compiled = fixture.nativeElement as HTMLElement;
  
    expect(compiled.querySelector('h1')?.textContent)
      .toContain('Job and Booking Information');
  
    expect(compiled.querySelector('mat-panel-title')?.textContent)
      .toContain('Job General Info');
  
    expect(compiled.querySelector('table.info-table'))
      .toBeTruthy();
  
    expect(compiled.querySelector('button[data-testid="cancel"]'))
      .toBeTruthy();
  });
});
