import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoiceStateRegressionConfirmerComponent } from './invoice-state-regression-confirmer.component';

describe('InvoiceStateRegressionConfirmerComponent', () => {
  let component: InvoiceStateRegressionConfirmerComponent;
  let fixture: ComponentFixture<InvoiceStateRegressionConfirmerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvoiceStateRegressionConfirmerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InvoiceStateRegressionConfirmerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
