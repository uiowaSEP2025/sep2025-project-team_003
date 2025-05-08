import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoiceJobComponent } from './invoice-job.component';

describe('InvoiceJobComponent', () => {
  let component: InvoiceJobComponent;
  let fixture: ComponentFixture<InvoiceJobComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvoiceJobComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InvoiceJobComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
