import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HeaderComponent } from './header.component';
import { ActivatedRoute, Router } from '@angular/router';
import { of, Subject } from 'rxjs';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { UserAuthService } from '../../services/user-auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

class MockUserAuthService {
  isLoggedIn$ = of(true);
  logout = jasmine.createSpy('logout').and.returnValue(of({}));
  setLoginStatus = jasmine.createSpy('setLoginStatus');
}

class MockMatSnackBar {
  open = jasmine.createSpy('open');
}

describe('HeaderComponent', () => {
  let component: HeaderComponent;
  let fixture: ComponentFixture<HeaderComponent>;
  let router: Router;
  let userAuth: MockUserAuthService;
  let snackBar: MockMatSnackBar;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeaderComponent],
      providers: [
        { provide: ActivatedRoute, useValue: { paramMap: of({}), queryParams: of({}) } },
        { provide: Router, useClass: MockRouter },
        { provide: UserAuthService, useClass: MockUserAuthService },
        { provide: MatSnackBar, useClass: MockMatSnackBar },
        provideHttpClient(),
        provideHttpClientTesting(),
        provideAnimationsAsync(),
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(HeaderComponent);
    component = fixture.componentInstance;
    router = TestBed.inject(Router);
    userAuth = TestBed.inject(UserAuthService) as unknown as MockUserAuthService;
    snackBar = TestBed.inject(MatSnackBar) as unknown as MockMatSnackBar;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should toggle the sidebarExpanded state', () => {
    expect(component.sidebarExpanded).toBeFalse();
    component.toggleSidebar();
    expect(component.sidebarExpanded).toBeTrue();
    component.toggleSidebar();
    expect(component.sidebarExpanded).toBeFalse();
  });

  it('should navigate to the correct page', () => {
    component.navigateToPage('login');
    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  });

  it('should logout and update login status', () => {
    component.onLogout();
    expect(userAuth.logout).toHaveBeenCalled();
    expect(snackBar.open).toHaveBeenCalledWith('Logout successfully!', '', { duration: 3000 });
    expect(userAuth.setLoginStatus).toHaveBeenCalledWith(false);
    expect(router.navigate).toHaveBeenCalledWith(['/login']);
  });
});
