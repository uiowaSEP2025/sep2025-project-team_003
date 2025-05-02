import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuotesDashboardPageComponent } from './quotes-dashboard-page.component';

describe('QuotesDashboardPageComponent', () => {
  let component: QuotesDashboardPageComponent;
  let fixture: ComponentFixture<QuotesDashboardPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QuotesDashboardPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuotesDashboardPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
