import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatButtonHarness } from '@angular/material/button/testing';
import { BookingJobsPerContractorComponent } from './booking-jobs-per-contractor.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';

describe('BookingJobsPerContractorComponent', () => {
  let component: BookingJobsPerContractorComponent;
  let fixture: ComponentFixture<BookingJobsPerContractorComponent>;
  let httpMock: HttpTestingController;
  let mockDialogRef: jasmine.SpyObj<MatDialogRef<BookingJobsPerContractorComponent>>;
  let loader: HarnessLoader;

  beforeEach(async () => {
    mockDialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);
    await TestBed.configureTestingModule({
      imports: [BookingJobsPerContractorComponent],
      providers: [provideAnimationsAsync(),
      provideHttpClient(),
      provideHttpClientTesting(),
      { provide: MAT_DIALOG_DATA, useValue: { contractorId: 1 } },
      { provide: MatDialogRef, useValue: mockDialogRef }
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(BookingJobsPerContractorComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    loader = TestbedHarnessEnvironment.loader(fixture);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch the right data', () => {
    const req = httpMock.expectOne('default/api/get/jobs/by-contractor?pagesize=5&offset=0&contractor=1');
    expect(req.request.method).toBe('GET');
    req.flush({ success: true });
  })

  it('should return the right data on close', async () => {
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Done' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter
    component.job = [1]
    await filteredButtons[0].click()
    fixture.detectChanges()
    expect(mockDialogRef.close).toHaveBeenCalledWith(1);
  })

  it('should return null on cancel', async () => {
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Exit' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter
    component.job = [1]
    await filteredButtons[0].click()
    fixture.detectChanges()
    expect(mockDialogRef.close).toHaveBeenCalledWith(null);
  })
});
