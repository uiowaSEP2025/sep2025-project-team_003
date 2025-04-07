import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateTemplateConfirmDialogComponentComponent } from './create-template-confirm-dialog-component.component';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}


describe('CreateTemplateConfirmDialogComponentComponent', () => {
  let component: CreateTemplateConfirmDialogComponentComponent;
  let fixture: ComponentFixture<CreateTemplateConfirmDialogComponentComponent>;
  let mockDialogRef: jasmine.SpyObj<MatDialogRef<CreateTemplateConfirmDialogComponentComponent>>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    mockDialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);

    await TestBed.configureTestingModule({
      imports: [CreateTemplateConfirmDialogComponentComponent],
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

    fixture = TestBed.createComponent(CreateTemplateConfirmDialogComponentComponent);
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call dialogRef.close with false when onCancel is called', () => {
    component.onCancel();
    expect(mockDialogRef.close).toHaveBeenCalledWith(false);
  });

  it('should call dialogRef.close with data when onConfirm is called', () => {
    component.onConfirm();
    expect(mockDialogRef.close).toHaveBeenCalledWith({
      description: null,
      name: "",
      services: undefined,
      materials: undefined
    });
  });
});
