import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ServicesCardComponent } from './services-card.component';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { of, Subject } from 'rxjs';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { provideRouter } from '@angular/router';

describe('ServicesCardComponent', () => {
  let component: ServicesCardComponent;
  let fixture: ComponentFixture<ServicesCardComponent>;
  let paramMapSubject: Subject<any>;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of({})
    };

    await TestBed.configureTestingModule({
      imports: [ServicesCardComponent, RouterModule],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRouteMock },
        provideAnimationsAsync(),
        provideHttpClient(withInterceptorsFromDi()),
        provideRouter([])
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ServicesCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
