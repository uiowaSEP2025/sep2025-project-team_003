import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

import { LoginComponent } from './login.component';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginComponent],
      providers: [provideAnimationsAsync()] 
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have the correct input fields', () => {
    const compiled = fixture.debugElement.nativeElement;
    const formfields = compiled.querySelectorAll('mat-form-field')
    expect(formfields[1].querySelector('mat-label').textContent).toContain('Password');
    expect(formfields[0].querySelector('mat-label').textContent).toContain('Username');
    
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const loginButton = buttonsArray.filter((el:Element) => (el.textContent == 'Login'))[0]
    const signUpButton = buttonsArray.filter((el:Element) => (el.textContent == 'Sign up'))[0]
    expect(loginButton).toBeTruthy();
    expect(signUpButton).toBeTruthy();
  });

  it('should be an invalid username when the username is empty', () => {
    const compiled = fixture.debugElement.nativeElement;
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const loginButton = buttonsArray.filter((el:Element) => (el.textContent == 'Login'))[0]
    expect(loginButton).toBeTruthy();
    (loginButton as HTMLElement).click();
    
    fixture.detectChanges(); // needed to detect the error field
    const errorTextElement = compiled.querySelectorAll('mat-form-field')[0].querySelector('mat-error')
    expect(errorTextElement.textContent).toEqual('Username is required');
  });

  it('should be an invalid password when the username is empty', () => {
    const compiled = fixture.debugElement.nativeElement;
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const loginButton = buttonsArray.filter((el:Element) => (el.textContent == 'Login'))[0]
    expect(loginButton).toBeTruthy();
    (loginButton as HTMLElement).click();
    
    fixture.detectChanges(); // needed to detect the error field
    const errorTextElement = compiled.querySelectorAll('mat-form-field')[1].querySelector('mat-error')
    expect(errorTextElement.textContent).toEqual('Password is required');
  });

  it('should be valid when username and password are there', () => {
    const compiled = fixture.debugElement.nativeElement;
    const buttonsArray:Element[] = Array.from(compiled.querySelectorAll('button'));
    const loginButton = buttonsArray.filter((el:Element) => (el.textContent == 'Login'))[0]
    expect(loginButton).toBeTruthy();
    (loginButton as HTMLElement).click();
    
    fixture.detectChanges(); // needed to detect the error field
    const passwordError = compiled.querySelectorAll('mat-form-field')[1].querySelector('mat-error');
    expect(errorTextElement).toEqual(null);
  });




});
