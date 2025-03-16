import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoiceDatePickerComponent } from './invoice-date-picker.component';

describe('InvoiceDatePickerComponent', () => {
  let component: InvoiceDatePickerComponent;
  let fixture: ComponentFixture<InvoiceDatePickerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvoiceDatePickerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InvoiceDatePickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
