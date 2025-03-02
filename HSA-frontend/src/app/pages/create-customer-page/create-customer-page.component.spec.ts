import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { CreateCustomerPageComponent } from './create-customer-page.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Router } from '@angular/router';


class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('CreateCustomerPageComponent', () => {
  let component: CreateCustomerPageComponent;
  let fixture: ComponentFixture<CreateCustomerPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateCustomerPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: Router, useClass: MockRouter }
      ]
    })
      .compileComponents();
    router = TestBed.inject(Router);

    fixture = TestBed.createComponent(CreateCustomerPageComponent);
    httpMock = TestBed.inject(HttpTestingController);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have the correct input fields', () => {
    const compiled = fixture.debugElement.nativeElement;
    const formfields = compiled.querySelectorAll('mat-form-field')
    expect(formfields[0].querySelector('mat-label').textContent).toEqual('First Name');
    expect(formfields[1].querySelector('mat-label').textContent).toEqual('Last Name');
    expect(formfields[2].querySelector('mat-label').textContent).toEqual('Email');
    expect(formfields[3].querySelector('mat-label').textContent).toEqual('Phone Number');
    expect(formfields[4].querySelector('mat-label').textContent).toEqual('Add Notes');

  })

  it('should display error when first name is missing', () => {
    const compiled = fixture.debugElement.nativeElement;
    const create = compiled.querySelector('button')
    const firstName = compiled.querySelectorAll('mat-form-field')[0]
    create.click()
    fixture.detectChanges()
    expect(firstName.querySelector('mat-error').textContent).toEqual('First Name is required')
  })

  it('should display error when last name is missing', () => {
    const compiled = fixture.debugElement.nativeElement;
    const create = compiled.querySelector('button')
    const lastName = compiled.querySelectorAll('mat-form-field')[1]
    create.click()
    fixture.detectChanges()
    expect(lastName.querySelector('mat-error').textContent).toEqual('Last Name is required')

  })

  it('should display error when email  is missing', () => {
    const compiled = fixture.debugElement.nativeElement;
    const create = compiled.querySelector('button')
    const email = compiled.querySelectorAll('mat-form-field')[2]
    create.click()
    fixture.detectChanges()
    expect(email.querySelector('mat-error').textContent).toEqual('Email is required')
  })

  it('should display error when email is invalid', () => {
    const compiled = fixture.debugElement.nativeElement;
    const create = compiled.querySelector('button')
    const email = compiled.querySelectorAll('mat-form-field')[2]
    const emailInput = email.querySelector('input')
    emailInput.value = 'a[egrodiKLS"mfndz'
    emailInput.dispatchEvent(new Event('input'));
    create.click()
    fixture.detectChanges()
    expect(email.querySelector('mat-error').textContent).toEqual('Email is invalid')
  })

  it('should display error when phone no is missing', () => {
    const compiled = fixture.debugElement.nativeElement;
    const create = compiled.querySelector('button')
    const phone = compiled.querySelectorAll('mat-form-field')[3]
    create.click()
    fixture.detectChanges()
    expect(phone.querySelector('mat-error').textContent).toEqual('Phone is required')
  })

  it('should display error when phone no is invalid', () => {
    const compiled = fixture.debugElement.nativeElement;
    const create = compiled.querySelector('button')
    const phone = compiled.querySelectorAll('mat-form-field')[3]
    const phoneInput = phone.querySelector('input')
    phoneInput.value = 'a[egrodiKLS"mfndz'
    phoneInput.dispatchEvent(new Event('input'));
    create.click()
    fixture.detectChanges()
    expect(phone.querySelector('mat-error').textContent).toEqual('Format is xxx-xxx-xxxx')
  })

  it('should be valid when everything is valid', () => {
    const compiled = fixture.debugElement.nativeElement;
    const create = compiled.querySelector('button')
    const firstNameinput = compiled.querySelectorAll('mat-form-field')[0].querySelector('input')
    firstNameinput.value = 'alex'
    firstNameinput.dispatchEvent(new Event('input'));
    const lastNameinput = compiled.querySelectorAll('mat-form-field')[1].querySelector('input')
    lastNameinput.value = 'guo'
    lastNameinput.dispatchEvent(new Event('input'));
    const emailInput = compiled.querySelectorAll('mat-form-field')[2].querySelector('input')
    emailInput.value = 'aguo2@uiowa.edu'
    emailInput.dispatchEvent(new Event('input'));
    lastNameinput.dispatchEvent(new Event('input'));
    const phoneInput = compiled.querySelectorAll('mat-form-field')[3].querySelector('input')
    phoneInput.value = '111-111-1111'
    phoneInput.dispatchEvent(new Event('input'));
    create.click()
    fixture.detectChanges()
    const errors = Array.from(compiled.querySelectorAll('mat-error'))
    expect(errors.length).toEqual(0)
  })

  describe('observables', () => {
    beforeEach(() => {
      const compiled = fixture.debugElement.nativeElement;
      const create = compiled.querySelector('button')
      const firstNameinput = compiled.querySelectorAll('mat-form-field')[0].querySelector('input')
      firstNameinput.value = 'alex'
      firstNameinput.dispatchEvent(new Event('input'));
      const lastNameinput = compiled.querySelectorAll('mat-form-field')[1].querySelector('input')
      lastNameinput.value = 'guo'
      lastNameinput.dispatchEvent(new Event('input'));
      const emailInput = compiled.querySelectorAll('mat-form-field')[2].querySelector('input')
      emailInput.value = 'aguo2@uiowa.edu'
      emailInput.dispatchEvent(new Event('input'));
      lastNameinput.dispatchEvent(new Event('input'));
      const phoneInput = compiled.querySelectorAll('mat-form-field')[3].querySelector('input')
      phoneInput.value = '111-111-1111'
      phoneInput.dispatchEvent(new Event('input'));
      create.click()
      fixture.detectChanges()
    }) 
  
    it('should navigate to login page on 401 unauthorized response', () => {
      const req = httpMock.expectOne(`${environment.apiUrl}/api/create/customer`);
      expect(req.request.method).toBe('POST');
      req.flush(null, { status: 401, statusText: 'Unauthorized' });
  
      expect(router.navigate).toHaveBeenCalledWith(['/login']);
    });
  
    it('should redirect to customers on successful response', () => {
      const req = httpMock.expectOne(`${environment.apiUrl}/api/create/customer`);
      expect(req.request.method).toBe('POST');
      req.flush(null, { status: 200, statusText: 'ok' });
      expect(router.navigate).toHaveBeenCalledWith(['/customers']);
  
    });
  })

  

});
