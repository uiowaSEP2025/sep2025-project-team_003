import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateServicePageComponent } from './create-service-page.component';

describe('CreateServicePageComponent', () => {
  let component: CreateServicePageComponent;
  let fixture: ComponentFixture<CreateServicePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateServicePageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateServicePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
