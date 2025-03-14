import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoiceQuotesDisplayTableComponent } from './invoice-quotes-display-table.component';

describe('InvoiceQuotesDisplayTableComponent', () => {
  let component: InvoiceQuotesDisplayTableComponent;
  let fixture: ComponentFixture<InvoiceQuotesDisplayTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvoiceQuotesDisplayTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InvoiceQuotesDisplayTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
