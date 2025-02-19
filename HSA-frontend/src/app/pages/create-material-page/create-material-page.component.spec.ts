import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateMaterialPageComponent } from './create-material-page.component';
import {provideAnimations} from '@angular/platform-browser/animations';

describe('CreateMaterialPageComponent', () => {
  let component: CreateMaterialPageComponent;
  let fixture: ComponentFixture<CreateMaterialPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateMaterialPageComponent],
      providers: [
        provideAnimations()
      ],
    })
    .compileComponents();

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
});
