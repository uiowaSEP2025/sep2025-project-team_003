import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContractorsHelperComponent } from './contractors-helper.component';

describe('ContractorsHelperComponent', () => {
  let component: ContractorsHelperComponent;
  let fixture: ComponentFixture<ContractorsHelperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContractorsHelperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContractorsHelperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
