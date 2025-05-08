import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { ViewInvoicePageComponent } from './view-invoice-page.component';
import { ActivatedRoute } from '@angular/router';
import { Invoice } from '../../components/invoice-job/invoice-job.component';
import { of, Subject } from 'rxjs';


describe('ViewInvoicePageComponent', () => {
  let component: ViewInvoicePageComponent;
  let fixture: ComponentFixture<ViewInvoicePageComponent>;
  let data: Invoice
  let paramMapSubject: Subject<any>;

  beforeEach(async () => {

    data = {
      id: 1,
      status: "Pending",
      dueDate: "2025-05-15",
      issuanceDate: "2025-05-01",
      customer: "John Doe",
      taxAmount: "15.50",
      taxPercent: "10",
      grandTotal: "155.50",
      url: "https://www.paypal.com",
      jobs: [
        {
          flatFee: 100,
          hourlyRate: 20,
          hoursWorked: 2.5,
          totalCost: 150,
          description: "Web development services"
        },
        {
          flatFee: 50,
          hourlyRate: 25,
          hoursWorked: 1,
          totalCost: 25,
          description: "Consulting services"
        }
      ]
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
