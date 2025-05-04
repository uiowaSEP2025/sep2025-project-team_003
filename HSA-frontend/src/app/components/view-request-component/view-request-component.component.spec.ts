import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewRequestComponentComponent } from './view-request-component.component';
import { of, Subject } from 'rxjs';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

class MatDialogRefMock {
  close() { }
}

describe('ViewRequestComponentComponent', () => {
  let component: ViewRequestComponentComponent;
  let fixture: ComponentFixture<ViewRequestComponentComponent>;
  let paramMapSubject: Subject<any>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of( {
        requestor_name: "",
        requestor_email: "",
        requestor_city: "",
        requestor_state: "",
        requestor_zip: "",
        requestor_address: "",
        description: "",
        status: ""
      })
    };

    const matDialogData = {
      info: {
        id: 1,
        requestor_name: "Test Name",
        requestor_email: "",
        requestor_city: "",
        requestor_state: "",
        requestor_zip: "",
        requestor_address: "",
        description: "",
        status: ""
      },
      status: ""
    }
      
    await TestBed.configureTestingModule({
      imports: [ViewRequestComponentComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(), 
        { provide: Router, useClass: MockRouter },
        { provide: ActivatedRoute, useValue: activatedRouteMock },
        { provide: MatDialogRef, useClass: MatDialogRefMock },
        { provide: MAT_DIALOG_DATA, useValue: matDialogData },
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewRequestComponentComponent);
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
