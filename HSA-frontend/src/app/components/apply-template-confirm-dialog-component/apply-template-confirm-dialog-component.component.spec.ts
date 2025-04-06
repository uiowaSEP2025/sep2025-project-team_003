import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApplyTemplateConfirmDialogComponentComponent } from './apply-template-confirm-dialog-component.component';

describe('ApplyTemplateConfirmDialogComponentComponent', () => {
  let component: ApplyTemplateConfirmDialogComponentComponent;
  let fixture: ComponentFixture<ApplyTemplateConfirmDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApplyTemplateConfirmDialogComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ApplyTemplateConfirmDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
