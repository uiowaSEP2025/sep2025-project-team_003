import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { of, Subject } from 'rxjs';

class MockRouter {
  public events = new Subject<any>();
}

describe('AppComponent', () => {
  let paramMapSubject: Subject<any>;
  let httpMock: HttpTestingController;
  let router: MockRouter;

  beforeEach(async () => {
    paramMapSubject = new Subject();
      const activatedRouteMock = {
        paramMap: paramMapSubject.asObservable(),
        queryParams: of({  })
      };

    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRouteMock },
        { provide: Router, useClass: MockRouter },
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    router = TestBed.inject(Router) as unknown as MockRouter;
    httpMock = TestBed.inject(HttpTestingController);

    fixture.detectChanges();
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should scroll to top on NavigationEnd event', () => {
    const fixture = TestBed.createComponent(AppComponent);
    router = TestBed.inject(Router) as unknown as MockRouter;

    const scrollToSpy = spyOn(window, 'scrollTo');
    fixture.detectChanges();

    router.events.next(new NavigationEnd(1, '/test', '/test'));
    expect(scrollToSpy).toHaveBeenCalled();

    const args = scrollToSpy.calls.mostRecent().args[0];
    expect(args).toEqual(jasmine.objectContaining({ top: 0, behavior: 'smooth' }));
  });
});