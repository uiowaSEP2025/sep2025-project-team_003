import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('AppComponent', () => {
  let httpMock: HttpTestingController;
  let router: Router;
  
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
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });
});
