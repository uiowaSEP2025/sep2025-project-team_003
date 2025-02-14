import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { ContractorsPageComponent } from './contractors-page.component';

describe('ContractorsPageComponent', () => {
  let component: ContractorsPageComponent;
  let fixture: ComponentFixture<ContractorsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContractorsPageComponent],
      providers: [provideAnimationsAsync()]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContractorsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
