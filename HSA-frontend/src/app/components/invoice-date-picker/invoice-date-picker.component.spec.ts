import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormGroup, FormControl } from '@angular/forms';
import { InvoiceDatePickerComponent } from './invoice-date-picker.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {MatDatepickerInputHarness} from '@angular/material/datepicker/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { DateRange } from '../../pages/edit-invoice-page/edit-invoice-page.component';

describe('InvoiceDatePickerComponent', () => {
  let component: InvoiceDatePickerComponent;
  let fixture: ComponentFixture<InvoiceDatePickerComponent>;
  let loader: HarnessLoader;
  let formGroup: FormGroup<DateRange>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvoiceDatePickerComponent],
      providers: [provideAnimationsAsync()]
    })
    .compileComponents();
    formGroup = new FormGroup({
      issued: new FormControl<Date | null>(null),
      due: new FormControl<Date | null>(null),
    });


    fixture = TestBed.createComponent(InvoiceDatePickerComponent);
    loader = TestbedHarnessEnvironment.loader(fixture);
    component = fixture.componentInstance;
    component.formControll = formGroup
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the components', async() => {
    const dateSelects = await loader.getAllHarnesses(MatDatepickerInputHarness);
    expect(dateSelects.length).toEqual(2)
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.textContent).toContain('Choose Dates')
  })

  it('should display error when date range invalid', () => {
    const compiled = fixture.debugElement.nativeElement;
    formGroup.controls.due.setValue(new Date("2021-03-25"))
    formGroup.controls.issued.setValue(new Date("2022-03-25"))
    fixture.detectChanges()
    expect(compiled.textContent).toContain('Please select a valid range')
  })

  it('should display error when no dates entered', () => {
    component.validate()
    fixture.detectChanges()
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.textContent).toContain('Please enter all values')
  })

  it('should display no error when date range valid', () => {
    const compiled = fixture.debugElement.nativeElement;
    formGroup.controls.due.setValue(new Date("2023-03-25"))
    formGroup.controls.issued.setValue(new Date("2022-03-25"))
    fixture.detectChanges()
    expect(compiled.textContent).not.toContain('Please select a valid range')
    expect(compiled.textContent).not.toContain('Please enter all values')
  })
});
