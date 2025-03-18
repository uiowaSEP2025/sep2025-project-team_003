import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { ViewInvoicePageComponent } from './view-invoice-page.component';
import { ActivatedRoute } from '@angular/router';
import { InvoiceDataInterface } from '../../interfaces/api-responses/invoice.api.data.interface';
import { of, Subject } from 'rxjs';


describe('ViewInvoicePageComponent', () => {
  let component: ViewInvoicePageComponent;
  let fixture: ComponentFixture<ViewInvoicePageComponent>;
  let data: InvoiceDataInterface
  let paramMapSubject: Subject<any>;

  beforeEach(async () => {

    data = {
      id: 1,
      status: "created",
      issuanceDate: "N/A",
      dueDate: "N/A",
      customer: "Alex Guo",
      quotes: {
        quotes: [],
        totalMaterialSubtotal: '0.00',
        totalPrice: '0.00'
      }
    }

    paramMapSubject = new Subject();
        const activatedRouteMock = {
          paramMap: of({
            get: (key: string) => '123' // Mock paramMap to return '123' for 'id'
          }),
          queryParams: of({ email: '', fname: '', lname: '', phoneNo: '' }),
          
        };

    await TestBed.configureTestingModule({
      imports: [ViewInvoicePageComponent],
      providers: [HttpClient, HttpHandler,
        { provide: ActivatedRoute, useValue: activatedRouteMock },
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ViewInvoicePageComponent);
    component = fixture.componentInstance;
    component.invoiceData = data
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render correctly', () => {
    const compiled = fixture.debugElement.nativeElement;
    const button = compiled.querySelector('button')
    expect(button).toBeTruthy()
    expect(compiled.textContent).toContain('Invoice for customer Alex Guo')
    expect(compiled.textContent).toContain('Invoice was issued: N/A')
    expect(compiled.textContent).toContain('Invoice is due: N/A')
    expect(compiled.textContent).toContain('Invoice status: created')
  })

  it('should set the invoice id correctly', () => {
    expect(component.invoiceID).toEqual(123)
  })
});
