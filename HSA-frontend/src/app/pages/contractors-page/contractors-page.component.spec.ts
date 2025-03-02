import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { ContractorsPageComponent } from './contractors-page.component';
import { Router } from '@angular/router';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('ContractorsPageComponent', () => {
  let component: ContractorsPageComponent;
  let fixture: ComponentFixture<ContractorsPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContractorsPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(), 
        { provide: Router, useClass: MockRouter }]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContractorsPageComponent);
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

  it('should navigate to login page on 401 unauthorized response', () => {
    const searchTerm = 'test';
    const pageSize = 10;
    const offSet = 0;
  
    component.loadDataToTable(searchTerm, pageSize, offSet);
  
    const req = httpMock.expectOne(`${environment.apiUrl}/api/get/contractors?search=${searchTerm}&pagesize=${pageSize}&offset=${offSet}`);
    expect(req.request.method).toBe('GET');
    req.flush(null, { status: 401, statusText: 'Unauthorized' });
  
    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  });

  it('should load data to table on successful response', () => {
    const mockResponse = [{ id: 1, name: 'Contractor 1' }, { id: 2, name: 'Contractor 2' }];
    const searchTerm = 'test';
    const pageSize = 10;
    const offSet = 0;
  
    component.loadDataToTable(searchTerm, pageSize, offSet);
  
    const req = httpMock.expectOne(`${environment.apiUrl}/api/get/contractors?search=${searchTerm}&pagesize=${pageSize}&offset=${offSet}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  
    expect(component.contractors).toEqual(mockResponse);
  });

  afterEach(() => {
    (router.navigate as jasmine.Spy).calls.reset();
  })
});
