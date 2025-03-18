import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { InvoicesPageComponent } from './invoices-page.component';
import { HttpClient } from '@angular/common/http';
import { HttpHandler } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

describe('InvoicesPageComponent', () => {
  let component: InvoicesPageComponent;
  let fixture: ComponentFixture<InvoicesPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvoicesPageComponent],
      providers: [provideHttpClientTesting(), HttpClient, HttpHandler, provideAnimationsAsync()]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InvoicesPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the compoenents', () => {
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('button')).toBeTruthy()
    expect(compiled.querySelector('table')).toBeTruthy()
  })
});
