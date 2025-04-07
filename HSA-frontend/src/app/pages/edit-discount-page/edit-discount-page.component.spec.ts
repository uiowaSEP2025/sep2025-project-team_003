import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditDiscountPageComponent } from './edit-discount-page.component';

describe('EditDiscountPageComponent', () => {
  let component: EditDiscountPageComponent;
  let fixture: ComponentFixture<EditDiscountPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditDiscountPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditDiscountPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
