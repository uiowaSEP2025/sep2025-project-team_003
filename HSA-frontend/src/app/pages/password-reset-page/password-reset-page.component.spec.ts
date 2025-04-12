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
import { MatInputHarness } from '@angular/material/input/testing';


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
    expect(passInput.length).toBeGreaterThan(0)
    expect(passConfirmInput.length).toBeGreaterThan(0)
    expect(submitButton).toBeTruthy()
  })

  it('should require the first password', async () => {
    const submitButton = await loader.getHarness(MatButtonHarness)
    await submitButton.click()
    const compiled = fixture.debugElement.nativeElement;

    const errors = Array.from(compiled.querySelectorAll('mat-error'));

    const requiredFirstPassError = (errors as HTMLElement[]).filter(
      (error) => error.textContent === "Password is required"
    );

    expect(requiredFirstPassError[0]).toBeTruthy()

  })

  it('should require the second password', async () => {
    const submitButton = await loader.getHarness(MatButtonHarness)
    await submitButton.click()
    const compiled = fixture.debugElement.nativeElement;

    const errors = Array.from(compiled.querySelectorAll('mat-error'));

    const requiredFirstPassError = (errors as HTMLElement[]).filter(
      (error) => error.textContent === "Password is required"
    );
    expect(requiredFirstPassError[1]).toBeTruthy()

  })

  describe('password strength checks', () => {

    it('should require a number', async () => {
      const submitButton = await loader.getHarness(MatButtonHarness)
      const compiled = fixture.debugElement.nativeElement;
      const passInput = await Promise.all(
        (await loader.getAllHarnesses(MatFormFieldHarness)).map(async (input) => {
          const text = await input.getLabel();
          return text === 'Password' ? input : null;
        })
      ).then(results => results.filter(input => input !== null)); // correctly working async filter

      const control = await passInput[0].getControl() as unknown as MatInputHarness;
      
      await control.setValue('aaaaaaaaA@')

      await submitButton.click()
      fixture.detectChanges()

      const errors = Array.from(compiled.querySelectorAll('mat-error'));
      const numberRequiredError = (errors as HTMLElement[]).filter(
        (error) => {
          return error.textContent!.includes("Must have 1 number")
        }
      );
      
      expect(numberRequiredError[0]).toBeTruthy()
    })

    it('should require a special character', async() => {
      const submitButton = await loader.getHarness(MatButtonHarness)
      const compiled = fixture.debugElement.nativeElement;
      const passInput = await Promise.all(
        (await loader.getAllHarnesses(MatFormFieldHarness)).map(async (input) => {
          const text = await input.getLabel();
          return text === 'Password' ? input : null;
        })
      ).then(results => results.filter(input => input !== null)); // correctly working async filter

      const control = await passInput[0].getControl() as unknown as MatInputHarness;
      
      await control.setValue('aaaaaaaaA1')

      await submitButton.click()
      fixture.detectChanges()

      const errors = Array.from(compiled.querySelectorAll('mat-error'));
      const specialCharRequiredError = (errors as HTMLElement[]).filter(
        (error) => {
          return error.textContent!.includes("Must have 1 special character")
        }
      );
      
      expect(specialCharRequiredError[0]).toBeTruthy()
    })

    it('should require an uppercase letter', async () => {
      const submitButton = await loader.getHarness(MatButtonHarness)
      const compiled = fixture.debugElement.nativeElement;
      const passInput = await Promise.all(
        (await loader.getAllHarnesses(MatFormFieldHarness)).map(async (input) => {
          const text = await input.getLabel();
          return text === 'Password' ? input : null;
        })
      ).then(results => results.filter(input => input !== null)); // correctly working async filter

      const control = await passInput[0].getControl() as unknown as MatInputHarness;
      
      await control.setValue('aaaaaaaa@1')

      await submitButton.click()
      fixture.detectChanges()

      const errors = Array.from(compiled.querySelectorAll('mat-error'));
      const uppercaseRequiredError = (errors as HTMLElement[]).filter(
        (error) => {
          return error.textContent!.includes("Must have 1 uppercase letter")
        }
      );
      
      expect(uppercaseRequiredError[0]).toBeTruthy()
    })
  })

  describe('password length checks', () => {

    it('should require length greater than 8', async () => {
      const submitButton = await loader.getHarness(MatButtonHarness)
      const compiled = fixture.debugElement.nativeElement;
      const passInput = await Promise.all(
        (await loader.getAllHarnesses(MatFormFieldHarness)).map(async (input) => {
          const text = await input.getLabel();
          return text === 'Password' ? input : null;
        })
      ).then(results => results.filter(input => input !== null)); // correctly working async filter

      const control = await passInput[0].getControl() as unknown as MatInputHarness;
      
      await control.setValue('a')

      await submitButton.click()
      fixture.detectChanges()

      const errors = Array.from(compiled.querySelectorAll('mat-error'));
      const tooShortError = (errors as HTMLElement[]).filter(
        (error) => {
          return error.textContent!.includes("Minimum 8 characters required")
        }
      );
      
      expect(tooShortError[0]).toBeTruthy()
      
    })

    it('should require length less than 16', async () => { 
      const submitButton = await loader.getHarness(MatButtonHarness)
      const compiled = fixture.debugElement.nativeElement;
      const passInput = await Promise.all(
        (await loader.getAllHarnesses(MatFormFieldHarness)).map(async (input) => {
          const text = await input.getLabel();
          return text === 'Password' ? input : null;
        })
      ).then(results => results.filter(input => input !== null)); // correctly working async filter

      const control = await passInput[0].getControl() as unknown as MatInputHarness;
      
      await control.setValue('1@Aaaaaaaaaaaaaaaaaaaaa')

      await submitButton.click()
      fixture.detectChanges()

      const errors = Array.from(compiled.querySelectorAll('mat-error'));
      const tooLongError = (errors as HTMLElement[]).filter(
        (error) => {
          return error.textContent!.includes("Maximum 16 characters required")
        }
      );
      
      expect(tooLongError[0]).toBeTruthy()

    })
    
  })

  it('should require the passwords to match', () => { })

  it('should call the correct endpoint when valid')

});
