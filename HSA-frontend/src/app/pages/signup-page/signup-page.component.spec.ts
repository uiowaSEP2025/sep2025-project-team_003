import { of, throwError } from 'rxjs';
import { UserAuthService } from '../../services/user-auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { RequestTrackerService } from '../../utils/request-tracker';
import { SignupPageComponent } from './signup-page.component';
import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter, Router } from '@angular/router';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('SignupPageComponent', () => {
  let component: SignupPageComponent;
  let router: Router;
  let fixture: ComponentFixture<SignupPageComponent>;
  let authService: jasmine.SpyObj<UserAuthService>;
  let dialog: jasmine.SpyObj<MatDialog>;

  beforeEach(async () => {
    const authSpy = jasmine.createSpyObj('UserAuthService', ['checkUserExist', 'createUser']);
    const snackBarSpy = jasmine.createSpyObj('MatSnackBar', ['open']);
    const dialogSpy = jasmine.createSpyObj('MatDialog', ['open']);
    const trackerSpy = jasmine.createSpyObj('RequestTrackerService', ['startRequest']);

    await TestBed.configureTestingModule({
      imports: [SignupPageComponent, NoopAnimationsModule],
      providers: [
        { provide: Router, useClass: MockRouter },
        { provide: UserAuthService, useValue: authSpy },
        { provide: MatSnackBar, useValue: snackBarSpy },
        { provide: MatDialog, useValue: dialogSpy },
        { provide: RequestTrackerService, useValue: trackerSpy },
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([])
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SignupPageComponent);
    router = TestBed.inject(Router);
    component = fixture.componentInstance;
    authService = TestBed.inject(UserAuthService) as jasmine.SpyObj<UserAuthService>;
    dialog = TestBed.inject(MatDialog) as jasmine.SpyObj<MatDialog>;
    fixture.detectChanges();
  });

  it('should call checkUserExist and move to next step if valid', () => {
    component.userAccountForm.setValue({
      userFirstName: 'John',
      userLastName: 'Doe',
      userEmail: 'john@example.com',
      username: 'johnuser',
      password: 'Test@1234',
      confirmPassword: 'Test@1234',
    });

    authService.checkUserExist.and.returnValue(of({ message: "" }));

    component.stepper = {
      selected: { completed: false },
      next: jasmine.createSpy('next')
    } as any;

    component.onSubmitUserCreation();

    expect(authService.checkUserExist).toHaveBeenCalled();
    expect(component.registrationForm.get('organizationEmail')?.value).toBe('john@example.com');
    expect(component.registrationForm.get('ownerName')?.value).toBe('John Doe');
    expect(component.stepper.next).toHaveBeenCalled();
  });

  it('should show error if username already exists', () => {
    component.userAccountForm.patchValue({
      username: 'existinguser',
      password: 'Test@1234'
    });
    authService.checkUserExist.and.returnValue(throwError(() => ({ status: 409 })));

    component.stepper = {
      selected: { completed: false },
      next: jasmine.createSpy('next')
    } as any;

    component.onSubmitUserCreation();
    expect(component.stepper.selected!.completed).toBeFalse();
  });

  it('should not call createUser if dialog is cancelled', fakeAsync(() => {
    dialog.open.and.returnValue({ afterClosed: () => of(false) } as any);

    component.onCreateConfirmDialog();
    tick();

    expect(authService.createUser).not.toHaveBeenCalled();
  }));

  it('should navigate to the correct page', () => {
    component.navigateToPage('login');
    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  });
});
