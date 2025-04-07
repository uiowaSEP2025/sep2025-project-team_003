import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ServicesHelperComponent } from './services-helper.component';

describe('ServicesHelperComponent', () => {
  let component: ServicesHelperComponent;
  let fixture: ComponentFixture<ServicesHelperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ServicesHelperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ServicesHelperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
