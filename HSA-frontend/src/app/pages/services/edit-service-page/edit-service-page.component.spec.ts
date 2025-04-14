import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EditServicePageComponent } from './edit-service-page.component';
import { Router, ActivatedRoute } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { of, Subject } from 'rxjs';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('EditServicePageComponent', () => {
  let component: EditServicePageComponent;
  let fixture: ComponentFixture<EditServicePageComponent>;
  let router: Router;
  let httpMock: HttpTestingController;
  let paramMapSubject: Subject<any>;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of({ material_name: 'larry' })
    };
    await TestBed.configureTestingModule({
      imports: [EditServicePageComponent],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRouteMock },
        { provide: Router, useClass: MockRouter },
        provideAnimations(),
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(EditServicePageComponent);
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
    const serviceFields = compiled.querySelectorAll('mat-form-field')
    expect(serviceFields[0].querySelector('mat-label').textContent).toEqual('New name');
    expect(serviceFields[1].querySelector('mat-label').textContent).toEqual('Description');
  })

  it('should display error when new name is missing', () => {
    const compiled = fixture.debugElement.nativeElement;
    const saveButton = compiled.querySelectorAll('button')[0]
    const newName = compiled.querySelectorAll('mat-form-field')[0]
    newName.value = '';
    saveButton.click()
    fixture.detectChanges()
    expect(newName.querySelector('mat-error').textContent).toEqual('Service Name is required')
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
