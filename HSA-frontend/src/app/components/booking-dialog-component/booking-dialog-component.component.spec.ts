import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { BookingDialogComponentComponent } from './booking-dialog-component.component';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatButtonHarness } from '@angular/material/button/testing';

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
        {
          provide: MatDialogRef,
          useValue: { close: jasmine.createSpy('close') }
        },
        {
          provide: MAT_DIALOG_DATA,
          useValue: { eventName: '', bookingType: '', jobID: null, jobDescription: "", status: "complete", backColor: "blue" }
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

  it('should return the correct value on close', () => { })

  it('should return the correct value on cancel', async  () => {
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
});
