import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { CreateServicePageComponent } from './create-service-page.component';
import {provideAnimations} from '@angular/platform-browser/animations';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('CreateServicePageComponent', () => {
  let component: CreateServicePageComponent;
  let fixture: ComponentFixture<CreateServicePageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateServicePageComponent],
      providers: [
        provideAnimations(),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: Router, useClass: MockRouter }
      ],
    })
    .compileComponents();
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(CreateServicePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have all input fields', () => {
    const compiled = fixture.debugElement.nativeElement;
    const serviceFields = compiled.querySelectorAll('mat-form-field');
    expect(serviceFields[0].querySelector('mat-label').textContent).toEqual('Service Name');
    expect(serviceFields[1].querySelector('mat-label').textContent).toEqual('Description');
  })

  it('should display error when service name is missing', () => {
    const compiled = fixture.debugElement.nativeElement;
    const createButton = compiled.querySelector('button');
    const serviceName = compiled.querySelectorAll('mat-form-field')[0];
    createButton.click();
    fixture.detectChanges();
    expect(serviceName.querySelector('mat-error').textContent).toEqual('Service Name is required');
  })

  it('should be valid when input fields are valid', () => {
    const compiled = fixture.debugElement.nativeElement;
    const createButton = compiled.querySelector('button');
    const serviceNameField = compiled.querySelectorAll('mat-form-field')[0].querySelector('input');
    serviceNameField.value = 'alex';
    serviceNameField.dispatchEvent(new Event('input'));
    const descriptionField = compiled.querySelectorAll('mat-form-field')[1].querySelector('textarea');
    descriptionField.value = 'guo';
    descriptionField.dispatchEvent(new Event('input'));
    createButton.click();
    fixture.detectChanges();

    const errorTexts = Array.from(compiled.querySelectorAll('mat-error'));
    expect(errorTexts.length).toEqual(0);
  })

  describe('observables', () => {
      beforeEach(() => {
        const compiled = fixture.debugElement.nativeElement;
        const createButton = compiled.querySelector('button');
        const materialNameField = compiled.querySelectorAll('mat-form-field')[0].querySelector('input');
        materialNameField.value = 'alex';
        materialNameField.dispatchEvent(new Event('input'));
        const descriptionField = compiled.querySelectorAll('mat-form-field')[1].querySelector('textarea');
        descriptionField.value = 'guo';
        descriptionField.dispatchEvent(new Event('input'));
        createButton.click();
        fixture.detectChanges();
  
      })
  
      it('should navigate to login page on 401 unauthorized response', () => {
        const req = httpMock.expectOne(`${environment.apiUrl}/api/create/service`);
        expect(req.request.method).toBe('POST');
        req.flush(null, { status: 401, statusText: 'Unauthorized' });
  
        expect(router.navigate).toHaveBeenCalledWith(['/login'], { queryParams: { prevPath: 'home' } });
      });
  
      it('should redirect to customers on successful response', () => {
        const req = httpMock.expectOne(`${environment.apiUrl}/api/create/service`);
        expect(req.request.method).toBe('POST');
        req.flush(null, { status: 200, statusText: 'ok' });
        expect(router.navigate).toHaveBeenCalledWith(['/services']);
  
      });
    })
});
