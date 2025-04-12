import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnboardingPageComponent } from './onboarding-page.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { of, Subject } from 'rxjs';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('OnboardingPageComponent', () => {
  let component: OnboardingPageComponent;
  let fixture: ComponentFixture<OnboardingPageComponent>;
  let paramMapSubject: Subject<any>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of({  })
    };

    await TestBed.configureTestingModule({
      imports: [OnboardingPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(), 
        { provide: Router, useClass: MockRouter },
        { provide: ActivatedRoute, useValue: activatedRouteMock },
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OnboardingPageComponent);
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render correctly', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const formFields = compiled.querySelectorAll('mat-form-field');
    expect(formFields[0].querySelector('mat-label').textContent).toContain('Service Name');
    expect(formFields[1].querySelector('mat-label').textContent).toContain('Service Description');
    expect(formFields[2].querySelector('mat-label').textContent).toContain('Customer First Name');
    expect(formFields[3].querySelector('mat-label').textContent).toContain('Customer Last Name');
    expect(formFields[4].querySelector('mat-label').textContent).toContain('Customer Email');
    expect(formFields[5].querySelector('mat-label').textContent).toContain('Customer Phone Number');
    expect(formFields[6].querySelector('mat-label').textContent).toContain('Add Notes');
    expect(formFields[7].querySelector('mat-label').textContent).toContain('Material Name');
    expect(formFields[8].querySelector('mat-label').textContent).toContain('Contractor First Name');
    expect(formFields[9].querySelector('mat-label').textContent).toContain('Contractor Last Name');
    expect(formFields[10].querySelector('mat-label').textContent).toContain('Contractor Email');
    expect(formFields[11].querySelector('mat-label').textContent).toContain('Contractor Phone Number');
    
    const jobFields = compiled.querySelectorAll('tr');
    expect(jobFields[0].querySelector('td').textContent).toContain('Customer*');
    expect(jobFields[1].querySelector('td').textContent).toContain('Start Date*');
    expect(jobFields[2].querySelector('td').textContent).toContain('End Date*');
    expect(jobFields[3].querySelector('td').textContent).toContain('Description*');
    expect(jobFields[4].querySelector('td').textContent).toContain('Address*');
    expect(jobFields[5].querySelector('td').textContent).toContain('City*');
    expect(jobFields[6].querySelector('td').textContent).toContain('State*');
    expect(jobFields[7].querySelector('td').textContent).toContain('Zip Code*');
  });

  it('should be an invalid fields when the fields are empty', () => {
    const compiled = fixture.debugElement.nativeElement;
    const formFields = compiled.querySelectorAll('mat-form-field');
    const jobFields = compiled.querySelectorAll('tr');
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const nextServiceButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[0];
    expect(nextServiceButton).toBeTruthy();
    (nextServiceButton as HTMLElement).click();
    fixture.detectChanges();

    expect(formFields[0].querySelector('mat-error').textContent).toEqual('Service Name is required');
    expect(formFields[1].querySelector('mat-error').textContent).toEqual('Service Description is required');
    (nextServiceButton as HTMLElement).click();
    fixture.detectChanges();

    const nextCustomerButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[1];
    expect(nextCustomerButton).toBeTruthy();
    (nextCustomerButton as HTMLElement).click();
    fixture.detectChanges();

    expect(formFields[2].querySelector('mat-error').textContent).toEqual('First Name is required');
    expect(formFields[3].querySelector('mat-error').textContent).toEqual('Last Name is required');
    expect(formFields[4].querySelector('mat-error').textContent).toEqual('Email is required');
    expect(formFields[5].querySelector('mat-error').textContent).toEqual('Phone is required');
    (nextCustomerButton as HTMLElement).click();
    fixture.detectChanges();

    const nextMaterialButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[2];
    expect(nextMaterialButton).toBeTruthy();
    (nextMaterialButton as HTMLElement).click();
    fixture.detectChanges();

    const nextContractor = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[3];
    expect(nextContractor).toBeTruthy();
    (nextContractor as HTMLElement).click();
    fixture.detectChanges();

    const selectCustomer = jobFields[0].querySelectorAll('td')[1].querySelector('button')
    expect(selectCustomer).toBeTruthy();
    expect(selectCustomer.textContent).toEqual('Select customer ')
    const nextJobGeneralButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[4];
    expect(nextJobGeneralButton).toBeTruthy();
    (nextJobGeneralButton as HTMLElement).click();
    fixture.detectChanges();
    
    expect(jobFields[0].querySelectorAll('td')[1].querySelector('mat-error').textContent).toEqual('Customer is required');
    expect(jobFields[1].querySelectorAll('td')[1].querySelector('mat-error').textContent).toEqual('Start date is required');
    expect(jobFields[3].querySelectorAll('td')[1].querySelector('mat-error').textContent).toEqual('Job description is required');
    expect(jobFields[4].querySelectorAll('td')[1].querySelector('mat-error').textContent).toEqual('Job assigned address is required');
    expect(jobFields[5].querySelectorAll('td')[1].querySelector('mat-error').textContent).toEqual('Job assigned city is required');
    expect(jobFields[6].querySelectorAll('td')[1].querySelector('mat-error').textContent).toEqual('State is required');
    expect(jobFields[7].querySelectorAll('td')[1].querySelector('mat-error').textContent).toEqual('Job assigned zip code is required');
    (nextJobGeneralButton as HTMLElement).click();
    fixture.detectChanges();

    const createButton = buttonsArray.filter((el:Element) => (el.textContent == 'Create'))[0];
    const cancelButton = buttonsArray.filter((el:Element) => (el.textContent == 'Cancel'))[0];
    expect(createButton).toBeTruthy();
    expect(cancelButton).toBeTruthy();
  });
});
