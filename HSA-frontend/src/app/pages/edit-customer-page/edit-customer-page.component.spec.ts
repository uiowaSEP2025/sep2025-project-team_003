import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditCustomerPageComponent } from './edit-customer-page.component';

describe('EditCustomerPageComponent', () => {
  let component: EditCustomerPageComponent;
  let fixture: ComponentFixture<EditCustomerPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditCustomerPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditCustomerPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
