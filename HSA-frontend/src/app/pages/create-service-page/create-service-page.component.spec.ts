import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateServicePageComponent } from './create-service-page.component';
import {provideAnimations} from '@angular/platform-browser/animations';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

describe('CreateServicePageComponent', () => {
  let component: CreateServicePageComponent;
  let fixture: ComponentFixture<CreateServicePageComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateServicePageComponent],
      providers: [
        provideAnimations(),
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    })
    .compileComponents();

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
});
