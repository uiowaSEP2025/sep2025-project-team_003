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
          useValue:  {
            "jobInfo": {
                "data": {
                    "id": 1,
                    "jobStatus": "completed",
                    "startDate": "2025-05-01",
                    "endDate": "2025-05-14",
                    "description": "Repair the plumbing system in the residential complex.",
                    "customerName": "First0 Last0",
                    "customerID": 1,
                    "requestorAddress": "2 W Washington St",
                    "requestorCity": "Iowa City",
                    "requestorState": "Iowa",
                    "requestorZip": "52240"
                },
                "services": [],
                "materials": [],
                "contractors": [
                    {
                        "id": 1,
                        "contractorID": 1,
                        "contractorName": "First0Con Last0Con",
                        "contractorPhoneNo": "801-981-8270",
                        "contractorEmail": "con0@example.com"
                    }
                ]
            },
            "bookingInfo": {
                "eventName": "sss",
                "status": "pending",
                "bookingType": "quote"
            }
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
