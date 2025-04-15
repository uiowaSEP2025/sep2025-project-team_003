import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnboardingSelectDialogComponentComponent } from './onboarding-select-dialog-component.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('OnboardingSelectDialogComponentComponent', () => {
  let component: OnboardingSelectDialogComponentComponent;
  let fixture: ComponentFixture<OnboardingSelectDialogComponentComponent>;
  let mockDialogRef: jasmine.SpyObj<MatDialogRef< OnboardingSelectDialogComponentComponent>>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    mockDialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);

    await TestBed.configureTestingModule({
      imports: [OnboardingSelectDialogComponentComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(), 
        { provide: Router, useClass: MockRouter },
        { provide: MatDialogRef, useValue: mockDialogRef },
        { provide: MAT_DIALOG_DATA, useValue: {} },
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OnboardingSelectDialogComponentComponent);
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call dialogRef.close with [] when onCancel is called', () => {
    component.onCancel();
    expect(mockDialogRef.close).toHaveBeenCalledWith([]);
  });

  it('should call dialogRef.close with data when onConfirm is called', () => {
    component.onConfirm();
    expect(mockDialogRef.close).toHaveBeenCalledWith({
      selectedItems: undefined,
      itemsInfo: []
    });
  });
});
