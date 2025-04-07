import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomersHelperComponent } from './customers-helper.component';

describe('CustomersHelperComponent', () => {
  let component: CustomersHelperComponent;
  let fixture: ComponentFixture<CustomersHelperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CustomersHelperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CustomersHelperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
