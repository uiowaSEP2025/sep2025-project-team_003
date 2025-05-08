import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MaterialsPageComponent } from './materials-page.component';
import { Router } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('MaterialsPageComponent', () => {
  let component: MaterialsPageComponent;
  let fixture: ComponentFixture<MaterialsPageComponent>;
  let router!: Router;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MaterialsPageComponent],
      providers: [
        provideAnimations(),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: Router, useClass: MockRouter }
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(MaterialsPageComponent);
    component = fixture.componentInstance;
    component.materials = []
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the components', () => {
    const compiled = fixture.debugElement.nativeElement;
    const table = compiled.querySelector('div[data-testid="app-table"]');
    const createButton = compiled.querySelector('button')
    expect(table).toBeTruthy()
    expect(createButton).toBeTruthy()
  })

  it('should navigate to add material page when click on add new material', () => {
    const compiled = fixture.debugElement.nativeElement;
    const addButton = compiled.querySelector('#add-material-button');

    addButton.click();
    fixture.detectChanges();
    expect(router.navigate).toHaveBeenCalledWith(['/materials/create']);
  });
});
