import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { PasswordResetPageComponent } from './password-reset-page.component';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatButtonHarness } from '@angular/material/button/testing';
import { MatFormFieldHarness } from '@angular/material/form-field/testing';


fdescribe('PasswordResetPageComponent', () => {
  let component: PasswordResetPageComponent;
  let fixture: ComponentFixture<PasswordResetPageComponent>;
  let loader: HarnessLoader;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PasswordResetPageComponent],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            queryParams: of({ token: 'mock-token' }) // simulate a token in the URL
          }
        },
        provideHttpClient(),
        provideHttpClientTesting(),
        provideAnimationsAsync(),
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(PasswordResetPageComponent);
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
    const title = compiled.querySelector('mat-card-header')
    const passInput = await Promise.all(
      (await loader.getAllHarnesses(MatFormFieldHarness)).map(async (input) => {
        const text = await input.getLabel();
        return text === 'Password' ? input : null;
      })
    ).then(results => results.filter(input => input !== null)); // correctly working async filter

    const passConfirmInput = await Promise.all(
      (await loader.getAllHarnesses(MatFormFieldHarness)).map(async (input) => {
        const text = await input.getLabel();
        return text === 'Confirm Password' ? input : null;
      })
    ).then(results => results.filter(input => input !== null)); // correctly working async filter
    
    expect(title.textContent).toContain('Reset Password')
    expect(passInput).toBeTruthy()
    expect(passConfirmInput).toBeTruthy()
    expect(submitButton).toBeTruthy()

  })

  it('should require the first password', () => { })

  it('should require the second password', () => { })

  describe('password strength checks', () => {

    it('should require a number', () => { })

    it('should require a special character', () => { })

    it('should require an uppercase letter', () => { })
  })

  it('should require the passwords to match', () => { })

  it('should call the correct endpoint when valid')

});
