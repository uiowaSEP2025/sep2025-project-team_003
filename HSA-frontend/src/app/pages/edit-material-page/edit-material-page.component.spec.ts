import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditMaterialPageComponent } from './edit-material-page.component';
import {provideRouter, Router} from '@angular/router';
import {provideAnimations} from '@angular/platform-browser/animations';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

describe('EditMaterialPageComponent', () => {
  let component: EditMaterialPageComponent;
  let fixture: ComponentFixture<EditMaterialPageComponent>;
  let router: Router;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditMaterialPageComponent],
      providers: [
        provideRouter([]),
        provideAnimations(),
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditMaterialPageComponent);
    component = fixture.componentInstance;
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
    const newName = compiled.querySelectorAll('mat-form-field')[0]
    newName.value = '';
    saveButton.click()
    fixture.detectChanges()
    expect(newName.querySelector('mat-error').textContent).toEqual('Material Name is required')
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
