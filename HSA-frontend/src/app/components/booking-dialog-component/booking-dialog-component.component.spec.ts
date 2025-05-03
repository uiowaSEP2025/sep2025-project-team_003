import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { BookingDialogComponentComponent } from './booking-dialog-component.component';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatButtonHarness } from '@angular/material/button/testing';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { MatSelectHarness } from '@angular/material/select/testing';

fdescribe('BookingDialogComponentComponent', () => {
  let component: BookingDialogComponentComponent;
  let fixture: ComponentFixture<BookingDialogComponentComponent>;
  let loader: HarnessLoader;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        BookingDialogComponentComponent,
        MatDialogModule,
      ],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
        {
          provide: MatDialogRef,
          useValue: { close: jasmine.createSpy('close') }
        },
        {
          provide: MAT_DIALOG_DATA,
          useValue: {
            startTime: "2025-04-30T10:30:00",
            endTime: "2025-04-30T15:00:00",
            typeOfDialog: "create",
            contractorId: 1
          }
        }
      ],
      schemas: [NO_ERRORS_SCHEMA]
    })
      .compileComponents();

    fixture = TestBed.createComponent(BookingDialogComponentComponent);
    loader = TestbedHarnessEnvironment.loader(fixture);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render all required form elements', () => {
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('h2')).toBeTruthy();
    expect(compiled.querySelector('input[formControlName="eventName"]')).toBeTruthy();
    expect(compiled.querySelector('mat-select[formControlName="bookingType"]')).toBeTruthy();
    expect(compiled.querySelector('mat-select[formControlName="status"]')).toBeTruthy();
    expect(compiled.querySelector('mat-select[formControlName="color"]')).toBeTruthy();
    expect(compiled.querySelector('[data-testid="cancel"]')).toBeTruthy();
    expect(compiled.querySelector('[data-testid="submit"]')).toBeTruthy();
  });

  it('should not be valid without a job id', async () => {
    const compiled = fixture.nativeElement;
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Submit' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)) // correctly working async filter
    const submit = filteredButtons[0]
    await submit.click()
    fixture.detectChanges()

    const errors = Array.from(compiled.querySelectorAll('mat-error')) as HTMLElement[];
    const error: HTMLElement[] = errors.filter((e) => {
      return e.textContent!.includes("Job ID is required")
    });

    expect(error).toBeTruthy()
  })

  it('should not be valid without a booking name', async () => {
    const compiled = fixture.nativeElement;
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Submit' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)) // correctly working async filter

    const submit = filteredButtons[0]
    await submit.click()

    fixture.detectChanges()

    const errors = Array.from(compiled.querySelectorAll('mat-error')) as HTMLElement[];
    const error: HTMLElement[] = errors.filter((e) => {
      return e.textContent!.includes("Event name is required")
    });

    expect(error).toBeTruthy()
  })

  it('should not be valid without a booking type', async () => {
    const compiled = fixture.nativeElement;
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Submit' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)) // correctly working async filter

    const submit = filteredButtons[0]
    await submit.click()

    fixture.detectChanges()

    const errors = Array.from(compiled.querySelectorAll('mat-error')) as HTMLElement[];
    const error: HTMLElement[] = errors.filter((e) => {
      return e.textContent!.includes("Booking type is required")
    });

    expect(error).toBeTruthy()

  })

  it('should return the correct value on close', async () => {
    component.eventForm.controls['jobID'].setValue!("2")
    component.eventForm.controls['bookingType'].setValue!("job")
    component.eventForm.controls['jobDescription'].setValue!("setting things on fire")
    component.eventForm.controls['status'].setValue!("pending")
    component.eventForm.controls['color'].setValue!("Green")
    component.eventForm.controls['eventName'].setValue!("demon")

    const compiled = fixture.nativeElement;
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Submit' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)) // correctly working async filter

    const submit = filteredButtons[0]
    await submit.click()
    fixture.detectChanges()

    expect(component.dialogRef.close).toHaveBeenCalledWith({
      eventName: 'demon',
      startTime: "2025-04-30T10:30:00",
      endTime: "2025-04-30T15:00:00",
      backColor: undefined,
      tags: {
        jobID: '2',
        jobDescription: 'setting things on fire',
        bookingType: 'job',
        status: 'pending'
      }
    });

  })

  it('should return the correct value on cancel', async () => {
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Cancel' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)) // correctly working async filter

    const cancel = filteredButtons[0]
    await cancel.click()

    expect(component.dialogRef.close).toHaveBeenCalledWith(false);

  })

  describe("time tests", () => {
    it('should update the end time on start time change', async () => {
      const startSelect = await loader.getHarness(MatSelectHarness.with({ selector: '[formControlName="startTime"]' }));
      const endSelect = await loader.getHarness(MatSelectHarness.with({ selector: '[formControlName="endTime"]' }));
      await endSelect.open();
      
      const endOptions = await endSelect.getOptions();
      await endOptions[1].click(); 

      await startSelect.open();
      const startOptions = await startSelect.getOptions();
      await startOptions[startOptions.length - 1].click();

      const value = await endSelect.getValueText()
      expect(value).toEqual("11:59 PM")
    })

    it('should update the start time on end time change', async () => {
      const startSelect = await loader.getHarness(MatSelectHarness.with({ selector: '[formControlName="startTime"]' }));
      const endSelect = await loader.getHarness(MatSelectHarness.with({ selector: '[formControlName="endTime"]' }));
      
      await startSelect.open();
      const startOptions = await startSelect.getOptions();
      await startOptions[startOptions.length - 1].click();

      
      await endSelect.open();
      
      const endOptions = await endSelect.getOptions();
      await endOptions[0].click(); 

      
      const value = await startSelect.getValueText()
      expect(value).toEqual("12:00 AM")
    })

  })
});
