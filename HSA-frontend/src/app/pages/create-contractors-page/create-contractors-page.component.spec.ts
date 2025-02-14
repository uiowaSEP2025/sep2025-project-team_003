import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateContractorsPageComponent } from './create-contractors-page.component';

describe('CreateContractorsPageComponent', () => {
  let component: CreateContractorsPageComponent;
  let fixture: ComponentFixture<CreateContractorsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateContractorsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateContractorsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
