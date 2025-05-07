import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdatePaymentPageComponent } from './update-payment-page.component';

describe('UpdatePaymentPageComponent', () => {
  let component: UpdatePaymentPageComponent;
  let fixture: ComponentFixture<UpdatePaymentPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UpdatePaymentPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UpdatePaymentPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
