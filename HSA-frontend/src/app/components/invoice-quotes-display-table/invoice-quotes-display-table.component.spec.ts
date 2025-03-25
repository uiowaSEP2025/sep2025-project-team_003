import { ComponentFixture, TestBed } from '@angular/core/testing';
import { InvoiceQuoteDisplayInterface } from '../../interfaces/api-responses/invoice.quote.display.interface';
import { InvoiceQuotesDisplayTableComponent } from './invoice-quotes-display-table.component';

describe('InvoiceQuotesDisplayTableComponent', () => {
  let component: InvoiceQuotesDisplayTableComponent;
  let fixture: ComponentFixture<InvoiceQuotesDisplayTableComponent>;
  let data: InvoiceQuoteDisplayInterface

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvoiceQuotesDisplayTableComponent]
    })
    .compileComponents();
    data = {
      'quotes': [
        {"materialSubtotal": "100",
        "totalPrice": "100",
        "jobDescription": "cat"},
        {"materialSubtotal": "200",
          "totalPrice": "200",
          "jobDescription": "dog"}],
        'totalMaterialSubtotal': "300",
        "subtotal": '$300.00',
        "taxPercent": '0.10',
    "totalDiscount": '0.10',
    "grandtotal" : '400.00',
    }

    fixture = TestBed.createComponent(InvoiceQuotesDisplayTableComponent);
    component = fixture.componentInstance;
    component.dataSource = data
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render correctly', () => {
    const compiled = fixture.debugElement.nativeElement;
    const rows = compiled.querySelectorAll('tr')
    const row0 = rows[0]
    const row1 = rows[1]
    const row2 = rows[2]
    const totals = rows[3]
    expect(row0.textContent).toContain('Job Description')
    expect(row0.textContent).toContain('Material Subtotal')
    expect(row0.textContent).toContain('Total Price')
    expect(row1.textContent).toContain('$100.00')
    expect(row1.textContent).toContain('cat')
    expect(row2.textContent).toContain('$200.00')
    expect(row2.textContent).toContain('dog')
    expect(totals.textContent).toContain('Subtotal:')
    expect(totals.textContent).toContain('$300.00')

  })
});
