import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddSelectDialogComponentComponent } from './add-select-dialog-component.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('AddSelectDialogComponentComponent', () => {
  let component: AddSelectDialogComponentComponent;
  let fixture: ComponentFixture<AddSelectDialogComponentComponent>;
  let mockDialogRef: jasmine.SpyObj<MatDialogRef<AddSelectDialogComponentComponent>>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    mockDialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);

    await TestBed.configureTestingModule({
      imports: [AddSelectDialogComponentComponent],
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

    fixture = TestBed.createComponent(AddSelectDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
