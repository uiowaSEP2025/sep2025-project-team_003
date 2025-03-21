import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddSelectDialogComponentComponent } from './add-select-dialog-component.component';

describe('AddSelectDialogComponentComponent', () => {
  let component: AddSelectDialogComponentComponent;
  let fixture: ComponentFixture<AddSelectDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddSelectDialogComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddSelectDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
