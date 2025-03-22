import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateConfirmDialogComponentComponent } from './update-confirm-dialog-component.component';

describe('UpdateConfirmDialogComponentComponent', () => {
  let component: UpdateConfirmDialogComponentComponent;
  let fixture: ComponentFixture<UpdateConfirmDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UpdateConfirmDialogComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UpdateConfirmDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
