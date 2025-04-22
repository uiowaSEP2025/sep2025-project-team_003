import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestDashboardPageComponent } from './request-dashboard-page.component';

describe('RequestDashboardPageComponent', () => {
  let component: RequestDashboardPageComponent;
  let fixture: ComponentFixture<RequestDashboardPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RequestDashboardPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RequestDashboardPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
