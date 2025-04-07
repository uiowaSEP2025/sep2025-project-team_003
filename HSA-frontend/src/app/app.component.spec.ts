import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { Subject } from 'rxjs';

class MockRouter {
  public events = new Subject<any>();
}

describe('AppComponent', () => {
  let httpMock: HttpTestingController;
  let router: MockRouter;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [
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
});