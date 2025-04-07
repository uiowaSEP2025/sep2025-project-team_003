import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiscountsHelperComponent } from './discounts-helper.component';

describe('DiscountsHelperComponent', () => {
  let component: DiscountsHelperComponent;
  let fixture: ComponentFixture<DiscountsHelperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DiscountsHelperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DiscountsHelperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
