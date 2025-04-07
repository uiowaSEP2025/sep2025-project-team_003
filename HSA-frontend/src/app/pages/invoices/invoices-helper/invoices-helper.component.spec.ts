import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoicesHelperComponent } from './invoices-helper.component';

describe('InvoicesHelperComponent', () => {
  let component: InvoicesHelperComponent;
  let fixture: ComponentFixture<InvoicesHelperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvoicesHelperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InvoicesHelperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
