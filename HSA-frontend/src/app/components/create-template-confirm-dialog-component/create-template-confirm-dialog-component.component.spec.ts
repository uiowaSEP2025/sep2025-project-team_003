import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateTemplateConfirmDialogComponentComponent } from './create-template-confirm-dialog-component.component';

describe('CreateTemplateConfirmDialogComponentComponent', () => {
  let component: CreateTemplateConfirmDialogComponentComponent;
  let fixture: ComponentFixture<CreateTemplateConfirmDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateTemplateConfirmDialogComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateTemplateConfirmDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
