import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ServicePageComponent } from './service-page.component';
import {provideRouter, Router} from '@angular/router';
import {provideAnimations} from '@angular/platform-browser/animations';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

describe('ServicePageComponent', () => {
  let component: ServicePageComponent;
  let fixture: ComponentFixture<ServicePageComponent>;
  let router!: Router;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ServicePageComponent],
      providers: [
        provideAnimations(),
        provideRouter([]),
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ServicePageComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    spyOn(router, "navigate").and.returnValue(Promise.resolve(true))
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

  it ('should navigate to create service page when click on add new service', () => {
    const compiled = fixture.debugElement.nativeElement;
    const addButton = compiled.querySelector('#add-service-button');

    addButton.click();
    fixture.detectChanges();
    expect(router.navigate).toHaveBeenCalledWith(['/services/create']);
  });

  it ('should navigate to material page when click on material list', () => {
    const compiled = fixture.debugElement.nativeElement;
    const materialListButton = compiled.querySelector('#material-list-button');

    materialListButton.click();
    fixture.detectChanges();
    expect(router.navigate).toHaveBeenCalledWith(['/materials']);
  });

  afterEach(() => {
    (router.navigate as jasmine.Spy).calls.reset();
  })
});
