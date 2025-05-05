import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { CustomersPageComponent } from './customers-page.component';
import { Router } from '@angular/router';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('CustomersPageComponent', () => {
  let component: CustomersPageComponent;
  let fixture: ComponentFixture<CustomersPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CustomersPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: Router, useClass: MockRouter }]
    })
      .compileComponents();

    fixture = TestBed.createComponent(CustomersPageComponent);
    component = fixture.componentInstance;
    component.customers = []
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

  



  afterEach(() => {
    (router.navigate as jasmine.Spy).calls.reset();
  })
});
