import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { RequestPasswordResetPageComponent } from './request-password-reset-page.component';

describe('RequestPasswordResetPageComponent', () => {
  let component: RequestPasswordResetPageComponent;
  let fixture: ComponentFixture<RequestPasswordResetPageComponent>;
  let loader: HarnessLoader;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RequestPasswordResetPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RequestPasswordResetPageComponent);
    component = fixture.componentInstance;
    loader = TestbedHarnessEnvironment.loader(fixture);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render correctly', () => {

  })

  it('should show the correct error when email is not provided', () => {})

  it('should show the correct error when email is invalid', () => {})

  it('should show call the correct endpoint when valid', () => {})
});
