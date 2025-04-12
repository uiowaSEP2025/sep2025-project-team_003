import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { RequestPasswordResetPageComponent } from './request-password-reset-page.component';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatButtonHarness } from '@angular/material/button/testing';
import { Router } from '@angular/router';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('RequestPasswordResetPageComponent', () => {
  let component: RequestPasswordResetPageComponent;
  let fixture: ComponentFixture<RequestPasswordResetPageComponent>;
  let loader: HarnessLoader;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RequestPasswordResetPageComponent],
      providers: [provideHttpClient(),
        provideHttpClientTesting(),
        provideAnimationsAsync(),
        { provide: Router, useClass: MockRouter }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RequestPasswordResetPageComponent);
    component = fixture.componentInstance;
    loader = TestbedHarnessEnvironment.loader(fixture);
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render correctly', async () => {
    const submitButton = await loader.getHarness(MatButtonHarness)
    const compiled = fixture.debugElement.nativeElement;
    const title = compiled.querySelector('mat-card-title')
    const input = compiled.querySelector('input')
    
    expect(await submitButton.getText()).toEqual("Send Reset Link")
    expect(title.textContent).toEqual('Reset your password')
    expect(input).toBeTruthy()
  })

  it('should show the correct error when email is not provided', async () => {
    const submitButton = await loader.getHarness(MatButtonHarness)
    const compiled = fixture.debugElement.nativeElement;

    await submitButton.click()
    fixture.detectChanges()

    const error = compiled.querySelector('mat-error')

    expect(error.textContent).toContain('Email is required')
  })

  it('should show the correct error when email is invalid', async () => {
    const submitButton = await loader.getHarness(MatButtonHarness)
    const compiled = fixture.debugElement.nativeElement;

    const email = compiled.querySelector('input');
    email.value = 'sergojijfd'

    email.dispatchEvent(new Event('input'));
    


    await submitButton.click()
    fixture.detectChanges()

    const error = compiled.querySelector('mat-error')

    expect(error.textContent).toContain('Please enter a valid email')

  })

  it('should call the correct endpoint when valid', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const emailInput = compiled.querySelector('input');
    const submitButton = await loader.getHarness(MatButtonHarness);
  
    const testEmail = 'test@example.com';
    emailInput.value = testEmail;
    emailInput.dispatchEvent(new Event('input'));
  
    await submitButton.click();
    fixture.detectChanges();
  
    const req = httpMock.expectOne('default/api/password_reset/');
    expect(req.request.method).toBe('POST');

    req.flush({ message: 'Success' });
    const router = TestBed.inject(Router) as jasmine.SpyObj<Router>;
    expect(router.navigate).toHaveBeenCalledWith(['/login']); // <-- update this path as needed

  
    httpMock.verify();
  });
  
});
