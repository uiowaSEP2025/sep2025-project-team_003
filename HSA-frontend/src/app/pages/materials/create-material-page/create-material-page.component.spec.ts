import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { CreateMaterialPageComponent } from './create-material-page.component';
import { provideAnimations } from '@angular/platform-browser/animations';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}
describe('CreateMaterialPageComponent', () => {
  let component: CreateMaterialPageComponent;
  let fixture: ComponentFixture<CreateMaterialPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateMaterialPageComponent],
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
    fixture = TestBed.createComponent(CreateMaterialPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have all input fields', () => {
    const compiled = fixture.debugElement.nativeElement;
    const materialFields = compiled.querySelectorAll('mat-form-field');
    expect(materialFields[0].querySelector('mat-label').textContent).toEqual('Material Name');
    expect(materialFields[1].querySelector('mat-label').textContent).toEqual('Description');
  })

  it('should display error when material name is missing', () => {
    const compiled = fixture.debugElement.nativeElement;
    const createButton = compiled.querySelector('button');
    const materialName = compiled.querySelectorAll('mat-form-field')[0];
    createButton.click();
    fixture.detectChanges();
    expect(materialName.querySelector('mat-error').textContent).toEqual('Material Name is required');
  })

  it('should be valid when input fields are valid', () => {
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
      const req = httpMock.expectOne(`${environment.apiUrl}/api/create/material`);
      expect(req.request.method).toBe('POST');
      req.flush(null, { status: 401, statusText: 'Unauthorized' });

      expect(router.navigate).toHaveBeenCalledWith(['/login'], { queryParams: { prevPath: 'home' } });
    });

    it('should redirect to customers on successful response', () => {
      const req = httpMock.expectOne(`${environment.apiUrl}/api/create/material`);
      expect(req.request.method).toBe('POST');
      req.flush(null, { status: 200, statusText: 'ok' });
      expect(router.navigate).toHaveBeenCalledWith(['/materials']);

    });
  })
});
