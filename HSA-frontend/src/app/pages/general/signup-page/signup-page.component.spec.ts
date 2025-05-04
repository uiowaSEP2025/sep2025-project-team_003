import {ComponentFixture, fakeAsync, TestBed, tick} from '@angular/core/testing';
import { SignupPageComponent } from './signup-page.component';
import {provideHttpClient} from '@angular/common/http';
import {HttpTestingController, provideHttpClientTesting} from '@angular/common/http/testing';
import {provideAnimations} from '@angular/platform-browser/animations';
import {provideRouter, Router} from '@angular/router';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { MatButtonHarness } from '@angular/material/button/testing';
import { MatFormFieldHarness } from '@angular/material/form-field/testing';
import { MatInputHarness } from '@angular/material/input/testing';


describe('SignupPageComponent', () => {
  let component: SignupPageComponent;
  let fixture: ComponentFixture<SignupPageComponent>;
  let httpMock: HttpTestingController;
  let router: Router;
  let loader: HarnessLoader;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SignupPageComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideAnimations(),
        provideRouter([])
      ],
    })
    .compileComponents();

    fixture = TestBed.createComponent(SignupPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    loader = TestbedHarnessEnvironment.loader(fixture);
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    spyOn(router, 'navigate').and.returnValue(Promise.resolve(true));

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have the correct input fields', () => {
    const compiled = fixture.debugElement.nativeElement;
    const formFields = compiled.querySelectorAll('mat-form-field');
    expect(formFields[0].querySelector('mat-label').textContent).toContain('User First Name');
    expect(formFields[1].querySelector('mat-label').textContent).toContain('User Last Name');
    expect(formFields[2].querySelector('mat-label').textContent).toContain('User Email');
    expect(formFields[3].querySelector('mat-label').textContent).toContain('Username');
    expect(formFields[4].querySelector('mat-label').textContent).toContain('Password');
    expect(formFields[5].querySelector('mat-label').textContent).toContain('Confirm Password');

    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const nextButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[0];
    const cancelButton = buttonsArray.filter((el:Element) => (el.textContent == 'Cancel'))[0];
    expect(nextButton).toBeTruthy();
    expect(cancelButton).toBeTruthy();
  });

  it('should be an invalid fields when the fields are empty', () => {
    const compiled = fixture.debugElement.nativeElement;
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const nextButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[0];
    expect(nextButton).toBeTruthy();
    (nextButton as HTMLElement).click();

    fixture.detectChanges(); // needed to detect the error field
    const firstNameErrorText = compiled.querySelectorAll('mat-form-field')[0].querySelector('mat-error');
    const lastNameErrorText = compiled.querySelectorAll('mat-form-field')[1].querySelector('mat-error');
    const emailErrorText = compiled.querySelectorAll('mat-form-field')[2].querySelector('mat-error');
    const usernameErrorText = compiled.querySelectorAll('mat-form-field')[3].querySelector('mat-error');
    const passwordErrorText = compiled.querySelectorAll('mat-form-field')[4].querySelector('mat-error');
    const confirmPasswordErrorText = compiled.querySelectorAll('mat-form-field')[5].querySelector('mat-error');
    expect(firstNameErrorText.textContent).toEqual('First Name is required');
    expect(lastNameErrorText.textContent).toEqual('Last Name is required');
    expect(emailErrorText.textContent).toEqual('Email is required');
    expect(usernameErrorText.textContent).toEqual('Username is required');
    expect(passwordErrorText.textContent).toEqual('Password is required');
    expect(confirmPasswordErrorText.textContent).toEqual('Password is required');
  });

  it('should be an invalid email', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const userEmailField = compiled.querySelectorAll('mat-form-field')[2];
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const nextButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[0];
    expect(nextButton).toBeTruthy();
    expect(userEmailField).toBeTruthy();

    const emailInput = userEmailField.querySelector('input');
    emailInput.value = "P";
    emailInput.dispatchEvent(new Event('input'));
    (nextButton as HTMLElement).click();

    fixture.detectChanges(); // needed to detect the error field
    const userEmailErrorText = compiled.querySelectorAll('mat-form-field')[2].querySelector('mat-error');
    expect(userEmailErrorText.textContent).toEqual('Email format is invalid');
  });

  it('should navigate to login page on cancel button', fakeAsync(() => {
    const compiled = fixture.debugElement.nativeElement;
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const cancelButton = buttonsArray.filter((el:Element) => (el.textContent == 'Cancel'))[0];

    (cancelButton as HTMLElement).click();
    tick();

    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  }));

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
 
    it('should require a special character', async () => {
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
 
  it('should require the passwords to match', async () => {
    const submitButton = await loader.getHarness(MatButtonHarness)
    const compiled = fixture.debugElement.nativeElement;
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
 
    const control1 = await passInput[0].getControl() as unknown as MatInputHarness;
    const control2 = await passConfirmInput[0].getControl() as unknown as MatInputHarness;
 
    await control1.setValue('SepTeam003!')
    await control2.setValue('SepTeam003!!!')
 
    await submitButton.click()
    fixture.detectChanges()
 
    const errors = Array.from(compiled.querySelectorAll('mat-error'));
    const matchingError = (errors as HTMLElement[]).filter(
      (error) => {
        return error.textContent!.includes("Password do not match")
      }
    );
 
    expect(matchingError[0]).toBeTruthy()
 
  })

  it('should have the correct input fields on 2nd page', () => {
    const compiled = fixture.debugElement.nativeElement;

    let buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    let nextButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[0];
    expect(nextButton).toBeTruthy();
    (nextButton as HTMLElement).click();
    
    const formFields = compiled.querySelectorAll('mat-form-field');
    expect(formFields[6].querySelector('mat-label').textContent).toContain('Organization Name');
    expect(formFields[7].querySelector('mat-label').textContent).toContain('Organization Email');
    expect(formFields[8].querySelector('mat-label').textContent).toContain('Primary phone');
    expect(formFields[9].querySelector('mat-label').textContent).toContain('Owner Name');

    buttonsArray = Array.from(compiled.querySelectorAll('button'));
    nextButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[0];
    const cancelButton = buttonsArray.filter((el:Element) => (el.textContent == 'Back'))[0];
    expect(nextButton).toBeTruthy();
    expect(cancelButton).toBeTruthy();
  });

  it('should have the correct input fields on 3rd page', () => {
    const compiled = fixture.debugElement.nativeElement;

    let buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    let nextButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[0];
    expect(nextButton).toBeTruthy();
    (nextButton as HTMLElement).click();
    
    const formFields = compiled.querySelectorAll('mat-form-field');
    expect(formFields[10].querySelector('mat-label').textContent).toContain('Address');
    expect(formFields[11].querySelector('mat-label').textContent).toContain('City');
    expect(formFields[12].querySelector('mat-label').textContent).toContain('State');
    expect(formFields[13].querySelector('mat-label').textContent).toContain('Zip Code');

    buttonsArray = Array.from(compiled.querySelectorAll('button'));
    nextButton = buttonsArray.filter((el:Element) => (el.textContent == 'Next'))[0];
    const cancelButton = buttonsArray.filter((el:Element) => (el.textContent == 'Back'))[0];
    expect(nextButton).toBeTruthy();
    expect(cancelButton).toBeTruthy();
  });


  afterEach(() => {
    httpMock.verify();
    (router.navigate as jasmine.Spy).calls.reset();
  });
});
