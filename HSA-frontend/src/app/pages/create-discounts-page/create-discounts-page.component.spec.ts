import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateDiscountsPageComponent } from './create-discounts-page.component';

describe('CreateDiscountsPageComponent', () => {
  let component: CreateDiscountsPageComponent;
  let fixture: ComponentFixture<CreateDiscountsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateDiscountsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateDiscountsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
