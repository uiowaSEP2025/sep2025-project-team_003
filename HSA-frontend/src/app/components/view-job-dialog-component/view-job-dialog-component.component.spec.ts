import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewJobDialogComponentComponent } from './view-job-dialog-component.component';

describe('ViewJobDialogComponentComponent', () => {
  let component: ViewJobDialogComponentComponent;
  let fixture: ComponentFixture<ViewJobDialogComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewJobDialogComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewJobDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
