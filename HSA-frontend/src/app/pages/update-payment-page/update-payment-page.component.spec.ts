import { ComponentFixture, TestBed } from '@angular/core/testing';
import {provideHttpClientTesting} from '@angular/common/http/testing';
import { UpdatePaymentPageComponent } from './update-payment-page.component';
import {provideHttpClient} from '@angular/common/http';
import {provideAnimations} from '@angular/platform-browser/animations';

describe('UpdatePaymentPageComponent', () => {
  let component: UpdatePaymentPageComponent;
  let fixture: ComponentFixture<UpdatePaymentPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UpdatePaymentPageComponent],
      providers: [provideHttpClient(),
        provideHttpClientTesting(),
      provideAnimations(),]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UpdatePaymentPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
