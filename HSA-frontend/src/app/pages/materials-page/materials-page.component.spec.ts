import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MaterialsPageComponent } from './materials-page.component';
import {provideRouter, Router} from '@angular/router';
import {provideAnimations} from '@angular/platform-browser/animations';

describe('MaterialsPageComponent', () => {
  let component: MaterialsPageComponent;
  let fixture: ComponentFixture<MaterialsPageComponent>;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MaterialsPageComponent],
      providers: [
        provideAnimations(),
        provideRouter([])
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MaterialsPageComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the components', () => {
    const compiled = fixture.debugElement.nativeElement;
    const table = compiled.querySelector('table')
    const createButton = compiled.querySelector('button')
    expect(table).toBeTruthy()
    expect(createButton).toBeTruthy()
  })

  it('should call router.navigate with the correct route when redirectCreate is called', () => {
    spyOn(router, "navigate")
    component.redirectCreate();
    expect(router.navigate).toHaveBeenCalledWith(['/materials/create']);
  });

  it ('should navigate to add material page when click on add new material', () => {
    const compiled = fixture.debugElement.nativeElement;
    const addButton = compiled.querySelector('#add-material-button');
    spyOn(router, "navigate")

    addButton.click();
    fixture.detectChanges();
    expect(router.navigate).toHaveBeenCalledWith(['/materials/create']);
  });
});
