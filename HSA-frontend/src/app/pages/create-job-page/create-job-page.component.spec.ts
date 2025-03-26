import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateJobPageComponent } from './create-job-page.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('CreateJobPageComponent', () => {
  let component: CreateJobPageComponent;
  let fixture: ComponentFixture<CreateJobPageComponent>;
  let httpMock: HttpTestingController;
  let router!: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateJobPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(), 
        { provide: Router, useClass: MockRouter }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateJobPageComponent);
    router = TestBed.inject(Router);
    httpMock = TestBed.inject(HttpTestingController);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
