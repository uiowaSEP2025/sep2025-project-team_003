import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiscountsPageComponent } from './discounts-page.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router } from '@angular/router';

describe('DiscountsPageComponent', () => {
  let component: DiscountsPageComponent;
  let fixture: ComponentFixture<DiscountsPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DiscountsPageComponent],
      providers: [provideAnimationsAsync(), provideHttpClient(), provideHttpClientTesting()]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DiscountsPageComponent);
    component = fixture.componentInstance;
    component.discounts = []
    fixture.detectChanges();
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });



  it('should render correctly', () => {
    const compiled = fixture.debugElement.nativeElement;
    const table = compiled.querySelector("app-table-component")
    const buttons = compiled.querySelectorAll('button')

    expect(table).toBeTruthy()

    const buttonsOutsideTable:any[] = Array.from(buttons).filter(button => {
      return !table || !table.contains(button);
    });

    expect(buttonsOutsideTable[0].textContent).toContain('Add a Discount')
  })

  it('clicking the create button should redirect to the create page', () => {
    spyOn(router, 'navigate');

    const compiled = fixture.debugElement.nativeElement;
    const buttons = compiled.querySelectorAll('button');
    const buttonsOutsideTable: any[] = Array.from(buttons).filter(button => {
      const table = compiled.querySelector("app-table-component");
      return !table || !table.contains(button);
    });
    const createButton = buttonsOutsideTable[0];

    createButton.click();
    expect(router.navigate).toHaveBeenCalledWith([ '/discounts/create' ]);
  })
});
