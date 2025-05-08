import { ComponentFixture, TestBed } from '@angular/core/testing';
import { environment } from '../../../environments/environment';
import { of, Subject } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { EditMaterialPageComponent } from './edit-material-page.component';
import { Router } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}


describe('EditMaterialPageComponent', () => {
  let component: EditMaterialPageComponent;
  let fixture: ComponentFixture<EditMaterialPageComponent>;
  let router: Router;
  let paramMapSubject: Subject<any>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of({ material_name: 'larry' })
    };
    await TestBed.configureTestingModule({
      imports: [EditMaterialPageComponent],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRouteMock },
        { provide: Router, useClass: MockRouter },
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(EditMaterialPageComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have all the input fields', () => {
    const compiled = fixture.debugElement.nativeElement;
    const materialFields = compiled.querySelectorAll('mat-form-field')
    expect(materialFields[0].querySelector('mat-label').textContent).toEqual('New name');
    expect(materialFields[1].querySelector('mat-label').textContent).toEqual('Description');
  })

  it('should display error when new name is missing', () => {
    const compiled = fixture.debugElement.nativeElement;
    const saveButton = compiled.querySelectorAll('button')[0]
    const newName = compiled.querySelectorAll('mat-form-field')[0].querySelector('input')
    newName.value = '';
    newName.dispatchEvent(new Event('input'));
    saveButton.click()
    fixture.detectChanges()
    expect(compiled.querySelectorAll('mat-form-field')[0].querySelector('mat-error').textContent).toEqual('Material Name is required')
  });

  it('should be valid when input fields are valid', () => {
    const compiled = fixture.debugElement.nativeElement;
    const saveButton = compiled.querySelectorAll('button')[0]
    const newNameField = compiled.querySelectorAll('mat-form-field')[0].querySelector('input')
    newNameField.value = 'alex'
    newNameField.dispatchEvent(new Event('input'));
    const descriptionField = compiled.querySelectorAll('mat-form-field')[1].querySelector('textarea')
    descriptionField.value = 'guo'
    descriptionField.dispatchEvent(new Event('input'));
    saveButton.click()
    fixture.detectChanges()

    const errors = Array.from(compiled.querySelectorAll('mat-error'))
    expect(errors.length).toEqual(0)
  });

  
});
