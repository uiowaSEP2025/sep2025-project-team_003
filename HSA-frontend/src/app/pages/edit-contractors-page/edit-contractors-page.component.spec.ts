import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditContractorsPageComponent } from './edit-contractors-page.component';

describe('EditContractorsPageComponent', () => {
  let component: EditContractorsPageComponent;
  let fixture: ComponentFixture<EditContractorsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditContractorsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditContractorsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
