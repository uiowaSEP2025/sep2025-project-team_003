import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestDashboardPageComponent } from './request-dashboard-page.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { of, Subject } from 'rxjs';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('RequestDashboardPageComponent', () => {
  let component: RequestDashboardPageComponent;
  let fixture: ComponentFixture<RequestDashboardPageComponent>;
  let paramMapSubject: Subject<any>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of( {
        id: 1,
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
      
    await TestBed.configureTestingModule({
      imports: [RequestDashboardPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(), 
        { provide: Router, useClass: MockRouter },
        { provide: ActivatedRoute, useValue: activatedRouteMock },
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RequestDashboardPageComponent);
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the components', () => {
    const compiled = fixture.debugElement.nativeElement;
    const table = compiled.querySelector('table')
    const createButton = compiled.querySelector('button')
    expect(table).toBeTruthy()
    expect(createButton).toBeTruthy()
  })
});
