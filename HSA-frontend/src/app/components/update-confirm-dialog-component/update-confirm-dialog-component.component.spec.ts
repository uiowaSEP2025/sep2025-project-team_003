import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateConfirmDialogComponentComponent } from './update-confirm-dialog-component.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('UpdateConfirmDialogComponentComponent', () => {
  let component: UpdateConfirmDialogComponentComponent;
  let fixture: ComponentFixture<UpdateConfirmDialogComponentComponent>;
  let mockDialogRef: jasmine.SpyObj<MatDialogRef<UpdateConfirmDialogComponentComponent>>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    mockDialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);

    await TestBed.configureTestingModule({
      imports: [UpdateConfirmDialogComponentComponent],
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

    fixture = TestBed.createComponent(UpdateConfirmDialogComponentComponent);
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
