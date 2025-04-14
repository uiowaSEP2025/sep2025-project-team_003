import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnboardingSelectDialogComponentComponent } from './onboarding-select-dialog-component.component';

describe('OnboardingSelectDialogComponentComponent', () => {
  let component: OnboardingSelectDialogComponentComponent;
  let fixture: ComponentFixture<OnboardingSelectDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OnboardingSelectDialogComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OnboardingSelectDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
