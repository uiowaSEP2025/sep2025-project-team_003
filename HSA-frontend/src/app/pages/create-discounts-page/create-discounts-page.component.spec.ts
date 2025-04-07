import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { CreateDiscountsPageComponent } from './create-discounts-page.component';
import { HarnessLoader } from '@angular/cdk/testing';
import { Router } from '@angular/router';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { MatButtonHarness } from '@angular/material/button/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';

fdescribe('CreateDiscountsPageComponent', () => {
  let component: CreateDiscountsPageComponent;
  let fixture: ComponentFixture<CreateDiscountsPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;
  let loader: HarnessLoader;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateDiscountsPageComponent],
      providers: [provideAnimationsAsync(), provideHttpClient(), provideHttpClientTesting()]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateDiscountsPageComponent);
    component = fixture.componentInstance;
    loader = TestbedHarnessEnvironment.loader(fixture);
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
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
  
      expect(name).toBeTruthy()
      expect(percent).toBeTruthy()
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
  
      const req = httpMock.expectOne('default/api/create/discount');
      expect(req.request.method).toBe('POST');
      
      // Verify the request body
      expect(req.request.body).toEqual({
        name: 'Christmas sale',
        percent: '22.00',
      });
      
    })
});
