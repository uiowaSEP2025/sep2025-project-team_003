import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { ContractorsPageComponent } from './contractors-page.component';
import { Router } from '@angular/router';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('ContractorsPageComponent', () => {
  let component: ContractorsPageComponent;
  let fixture: ComponentFixture<ContractorsPageComponent>;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContractorsPageComponent],
      providers: [provideAnimationsAsync(), { provide: Router, useClass: MockRouter }]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContractorsPageComponent);
    router = TestBed.inject(Router);
    component = fixture.componentInstance;
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
    component.redirectCreate();
    expect(router.navigate).toHaveBeenCalledWith(['/contractors/create']);
  });

});
