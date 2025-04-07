import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { EditDiscountPageComponent } from './edit-discount-page.component';
import { HttpTestingController } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { of, Subject } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatButtonHarness } from '@angular/material/button/testing';
import { convertToParamMap } from '@angular/router';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}


fdescribe('EditDiscountPageComponent', () => {
  let component: EditDiscountPageComponent;
  let fixture: ComponentFixture<EditDiscountPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;
  let loader: HarnessLoader;
  let paramMapSubject: Subject<any>;

  paramMapSubject = new Subject();
        const activatedRouteMock = {
          paramMap: of(convertToParamMap({ id: '1' })),
          queryParams: of({ 
            "discount_percent": "20.00 %",
            "discount_name": "Summer Sale"
           }),
           
        };
  

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditDiscountPageComponent],
      providers: [provideHttpClient(),
              provideHttpClientTesting(),
              { provide: Router, useClass: MockRouter },
            { provide: ActivatedRoute, useValue: activatedRouteMock },
            provideAnimationsAsync()]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditDiscountPageComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
    loader = TestbedHarnessEnvironment.loader(fixture);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render correctly', () => {
    const compiled = fixture.debugElement.nativeElement;
    const inputs = compiled.querySelectorAll('input')
    const submitButton = compiled.querySelector('button')
    const name = inputs[0]
    const percent = inputs[1]

    expect(name.value).toEqual("Summer Sale")
    expect(percent.value).toEqual("20.00")
    expect(submitButton).toBeTruthy()
  })

  it('should be invalid without a name', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const submitButton = await loader.getHarness(MatButtonHarness);
    const inputs = compiled.querySelectorAll('input')
    const name = inputs[0]
    const percent = inputs[1]
    name.value = ""
    name.dispatchEvent(new Event('input'));
    percent.value = "20.00"
    percent.dispatchEvent(new Event('input'));
    await submitButton.click()
    fixture.detectChanges()

    const error = compiled.querySelector('mat-error')

    expect(error.textContent).toEqual("Name is required")
    
  })

  it('should be invalid without a percent', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const submitButton = await loader.getHarness(MatButtonHarness);
    const inputs = compiled.querySelectorAll('input')
    const name = inputs[0]
    const percent = inputs[1]
    name.value = "Christmas sale"
    name.dispatchEvent(new Event('input'));
    percent.value = ""
    percent.dispatchEvent(new Event('input'));
    await submitButton.click()
    fixture.detectChanges()

    const error = compiled.querySelector('mat-error')
    expect(error.textContent).toEqual("Discount percent is required")
    
  })

  it('should be invalid with an invalid percent', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const submitButton = await loader.getHarness(MatButtonHarness);
    const inputs = compiled.querySelectorAll('input')
    const name = inputs[0]
    const percent = inputs[1]
    name.value = "Christmas sale"
    name.dispatchEvent(new Event('input'));
    percent.value = "223222"
    percent.dispatchEvent(new Event('input'));
    await submitButton.click()
    fixture.detectChanges()

    const error = compiled.querySelector('mat-error')

    expect(error.textContent).toEqual("Discount percent must be xx.xx")
  })

  it('should call to the endpoint when a valid submit happens', async() => {
    const compiled = fixture.debugElement.nativeElement;
    const submitButton = await loader.getHarness(MatButtonHarness);
    const inputs = compiled.querySelectorAll('input')
    const name = inputs[0]
    const percent = inputs[1]
    name.value = "Christmas sale"
    name.dispatchEvent(new Event('input'));
    percent.value = "22.00"
    percent.dispatchEvent(new Event('input'));
    await submitButton.click()
    fixture.detectChanges()

    const error = compiled.querySelector('mat-error')

    expect(error).toBeFalsy()

    const req = httpMock.expectOne('default/api/edit/discount/1'); // Adjust the URL if needed
    expect(req.request.method).toBe('POST');
    
    // Verify the request body
    expect(req.request.body).toEqual({
      name: 'Christmas sale',
      percent: '22.00',
      id: '1'
    });
    
  })
});
