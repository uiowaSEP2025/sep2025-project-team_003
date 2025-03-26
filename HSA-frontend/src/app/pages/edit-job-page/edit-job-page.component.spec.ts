import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditJobPageComponent } from './edit-job-page.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { of, Subject } from 'rxjs';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('EditJobPageComponent', () => {
  let component: EditJobPageComponent;
  let fixture: ComponentFixture<EditJobPageComponent>;
  let paramMapSubject: Subject<any>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of( {
          jobStatus: "",
          startDate: "",
          endDate: "",
          description: "",
          customerID: 1, 
          city: "",
          state: "",
          zip: "",
          address: ""
      })
    };

    await TestBed.configureTestingModule({
      imports: [EditJobPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(), 
        { provide: Router, useClass: MockRouter },
        { provide: ActivatedRoute, useValue: activatedRouteMock },
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditJobPageComponent);
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
