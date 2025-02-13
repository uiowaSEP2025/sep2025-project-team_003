import {ComponentFixture, fakeAsync, TestBed, tick} from '@angular/core/testing';
import { SignupPageComponent } from './signup-page.component';
import {provideHttpClient} from '@angular/common/http';
import {HttpTestingController, provideHttpClientTesting} from '@angular/common/http/testing';
import {provideAnimations} from '@angular/platform-browser/animations';
import {provideRouter, Router} from '@angular/router';


describe('SignupPageComponent', () => {
  let component: SignupPageComponent;
  let fixture: ComponentFixture<SignupPageComponent>;
  let httpMock: HttpTestingController;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SignupPageComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideAnimations(),
        provideRouter([])
      ],
    })
    .compileComponents();

    fixture = TestBed.createComponent(SignupPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);

    spyOn(component, "ngOnInit").and.callFake(() => {
      component.loadStates();
    });

    fixture.detectChanges();
  });

  it('should create', () => {
    const request = httpMock.expectOne('states.json');
    expect(request.request.method).toBe('GET');
    expect(component).toBeTruthy();
    httpMock.verify();
  });

  it('should have the correct input fields', () => {
    const compiled = fixture.debugElement.nativeElement;
    const request = httpMock.expectOne('states.json');
    expect(request.request.method).toBe('GET');
    const formFields = compiled.querySelectorAll('mat-form-field');
    expect(formFields[0].querySelector('mat-label').textContent).toContain('Organization Name');
    expect(formFields[1].querySelector('mat-label').textContent).toContain('Organization Email');
    expect(formFields[2].querySelector('mat-label').textContent).toContain('Address 1');
    expect(formFields[3].querySelector('mat-label').textContent).toContain('Address 2');
    expect(formFields[4].querySelector('mat-label').textContent).toContain('City');
    expect(formFields[5].querySelector('mat-label').textContent).toContain('State');
    expect(formFields[6].querySelector('mat-label').textContent).toContain('Owner Name');

    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const createButton = buttonsArray.filter((el:Element) => (el.textContent == 'Create'))[0];
    const cancelButton = buttonsArray.filter((el:Element) => (el.textContent == 'Cancel'))[0];
    expect(createButton).toBeTruthy();
    expect(cancelButton).toBeTruthy();
  });

  it('should fetch the state json request', () => {
    const mockData = [
      { name:  "Georgia", code:  "GA"},
      { name:  "Hawaii", code:  "HI"},
      { name:  "Idaho", code:  "ID"}
    ];

    //Expect HTTP request and flush the data as response
    const request = httpMock.expectOne('states.json');
    expect(request.request.method).toBe('GET');
    request.flush(mockData);

    //Check the json contents
    expect(component.states).toEqual(mockData);

    httpMock.verify();
  });

  it('should populate the state selector on page', () => {
    const mockData = [
      { name:  "Georgia", code:  "GA"},
      { name:  "Idaho", code:  "ID"}
    ];

    const request = httpMock.expectOne('states.json');
    expect(request.request.method).toBe('GET');
    request.flush(mockData);

    expect(component.states).toEqual(mockData);
    expect(component.states.length).toEqual(2);

    httpMock.verify();
  });

  it('should be an invalid fields when the fields are empty', () => {
    const compiled = fixture.debugElement.nativeElement;
    const request = httpMock.expectOne('states.json');
    expect(request.request.method).toBe('GET');
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const createButton = buttonsArray.filter((el:Element) => (el.textContent == 'Create'))[0];
    expect(createButton).toBeTruthy();
    (createButton as HTMLElement).click();

    fixture.detectChanges(); // needed to detect the error field
    const organizationNameErrorText = compiled.querySelectorAll('mat-form-field')[0].querySelector('mat-error');
    const organizationEmailErrorText = compiled.querySelectorAll('mat-form-field')[1].querySelector('mat-error');
    const addressOneErrorText = compiled.querySelectorAll('mat-form-field')[2].querySelector('mat-error');
    const stateErrorText = compiled.querySelectorAll('mat-form-field')[5].querySelector('mat-error');
    const ownerNameErrorText = compiled.querySelectorAll('mat-form-field')[6].querySelector('mat-error');
    expect(organizationNameErrorText.textContent).toEqual('Organization Name is required');
    expect(organizationEmailErrorText.textContent).toEqual('Organization Email is required');
    expect(addressOneErrorText.textContent).toEqual('Primary Address is required');
    expect(stateErrorText.textContent).toEqual('State is required');
    expect(ownerNameErrorText.textContent).toEqual('Valid Owner is required');
  });

  it('should be an invalid email', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const request = httpMock.expectOne('states.json');
    expect(request.request.method).toBe('GET');
    const organizationEmailField = compiled.querySelectorAll('mat-form-field')[1];
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const createButton = buttonsArray.filter((el:Element) => (el.textContent == 'Create'))[0];
    expect(createButton).toBeTruthy();
    expect(organizationEmailField).toBeTruthy();

    const emailInput = organizationEmailField.querySelector('input');
    emailInput.value = "P";
    emailInput.dispatchEvent(new Event('input'));
    (createButton as HTMLElement).click();

    fixture.detectChanges(); // needed to detect the error field
    const organizationEmailErrorText = compiled.querySelectorAll('mat-form-field')[1].querySelector('mat-error');
    expect(organizationEmailErrorText.textContent).toEqual('Email format is invalid');
  });

  it('should navigate to home page on cancel button', fakeAsync(() => {
    const compiled = fixture.debugElement.nativeElement;
    const request = httpMock.expectOne('states.json');
    expect(request.request.method).toBe('GET');
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const cancelButton = buttonsArray.filter((el:Element) => (el.textContent == 'Cancel'))[0];

    spyOn(router, 'navigate');
    (cancelButton as HTMLElement).click();
    tick();

    expect(router.navigate).toHaveBeenCalledWith(['/home']);
  }));

  afterEach(() => {
    httpMock.verify();
  });
});
