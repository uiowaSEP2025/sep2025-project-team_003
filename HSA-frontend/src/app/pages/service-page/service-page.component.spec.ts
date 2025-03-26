import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ServicePageComponent } from './service-page.component';
import { Router } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('ServicePageComponent', () => {
  let component: ServicePageComponent;
  let fixture: ComponentFixture<ServicePageComponent>;
  let router!: Router;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ServicePageComponent],
      providers: [
        provideAnimations(),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: Router, useClass: MockRouter }
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ServicePageComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
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

  it('should navigate to create service page when click on add new service', () => {
    const compiled = fixture.debugElement.nativeElement;
    const addButton = compiled.querySelector('#add-service-button');

    addButton.click();
    fixture.detectChanges();
    expect(router.navigate).toHaveBeenCalledWith(['/services/create']);
  });

  describe('observable', () => {
    it('should navigate to login page on 401 unauthorized response', () => {
      const searchTerm = 'test';
      const pageSize = 10;
      const offSet = 0;

      component.loadDataToTable(searchTerm, pageSize, offSet);

      const req = httpMock.expectOne(`${environment.apiUrl}/api/get/services?search=${searchTerm}&pagesize=${pageSize}&offset=${offSet}`);
      expect(req.request.method).toBe('GET');
      req.flush(null, { status: 401, statusText: 'Unauthorized' });

      expect(router.navigate).toHaveBeenCalledWith(['/login'], { queryParams: { prevPath: 'services' } });
    });

    it('should load data to table on successful response', () => {
      const mockResponse = [{ id: 1, name: 'Contractor 1' }, { id: 2, name: 'Contractor 2' }];
      const searchTerm = 'test';
      const pageSize = 10;
      const offSet = 0;

      component.loadDataToTable(searchTerm, pageSize, offSet);

      const req = httpMock.expectOne(`${environment.apiUrl}/api/get/services?search=${searchTerm}&pagesize=${pageSize}&offset=${offSet}`);
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);

      expect(component.services).toEqual(mockResponse);
    });
  })
  afterEach(() => {
    (router.navigate as jasmine.Spy).calls.reset();
  })
});
