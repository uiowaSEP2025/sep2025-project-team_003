import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { ViewInvoicePageComponent } from './view-invoice-page.component';
import { ActivatedRoute } from '@angular/router';
import { InvoiceDataInterface } from '../../../interfaces/api-responses/invoice.api.data.interface';
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
      dateIssued: "N/A",
      dateDue: "N/A",
      customer: {
        first_name: "Alex",
        last_name: "Guo",
        notes: "",
        email: "",
        id: 0,
        phone: ""

      },
      quotes: {
        quotes: [],
        totalMaterialSubtotal: '0.00',
        subtotal: '0.00',
        taxPercent: '0.00',
        totalDiscount: '0.00',
        "grandtotal" : 'O.00'
      },
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
    expect(compiled.textContent).toContain('Customer')
    expect(compiled.textContent).toContain('Issued Date')
    expect(compiled.textContent).toContain('Due Date')
    expect(compiled.textContent).toContain('Status')
  })

  it('should set the invoice id correctly', () => {
    expect(component.invoiceID).toEqual(123)
  })
});
