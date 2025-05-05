import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClient } from '@angular/common/http';
import { EditInvoicePageComponent } from './edit-invoice-page.component';
import { HttpHandler } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { Subject, of } from 'rxjs';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatSelectHarness } from '@angular/material/select/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { MatButtonHarness } from '@angular/material/button/testing';
import { InvoiceService } from '../../services/invoice.service';

describe('EditInvoicePageComponent', () => {
  let component: EditInvoicePageComponent;
  let fixture: ComponentFixture<EditInvoicePageComponent>;
  let paramMapSubject: Subject<any>;
  let loader: HarnessLoader;
  let invoiceService: InvoiceService;

  paramMapSubject = new Subject();
      const activatedRouteMock = {
        paramMap: paramMapSubject.asObservable(),
        queryParams: of({ status: 'created',
            "due_date": "N/A",
            "issuance_date": "N/A",
            "customer": "Alex Guo",
            "tax":"0.06"
         })
      };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditInvoicePageComponent],
      providers: [HttpClient, HttpHandler,  { provide: ActivatedRoute, useValue: activatedRouteMock }, provideAnimationsAsync()]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditInvoicePageComponent);
    component = fixture.componentInstance;
    loader = TestbedHarnessEnvironment.loader(fixture);
    invoiceService = TestBed.inject(InvoiceService);
    component.tax = 0.06
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display date picker when status is not created', async () => {
    const select = (await loader.getAllHarnesses(MatSelectHarness))[0]
    const compiled = fixture.debugElement.nativeElement;
    await select.open();
    const options = await select.getOptions();
    await options[2].click()
    fixture.detectChanges()
    expect(compiled.textContent).toContain("Choose Dates")
  })

  it('should not display date picker when status is created', async () => {
    const compiled = fixture.debugElement.nativeElement;
    fixture.detectChanges()
    expect(compiled.textContent).not.toContain("Choose Dates")
  })

  it('should call validate on the view child', async () => {
    const select = (await loader.getAllHarnesses(MatSelectHarness))[0]
    await select.open();
    const options = await select.getOptions();
    await options[1].click()
    fixture.detectChanges()
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Submit' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter
    spyOn(component.datePicker, 'validate'); // Spy on the function

    const submit = filteredButtons[0]; 
    await submit.click()
    fixture.detectChanges()

    expect(component.datePicker.validate).toHaveBeenCalled(); // Verify the call
  })

  it('should show error when no quotes are selected', async () => {
    const compiled = fixture.debugElement.nativeElement;
    fixture.detectChanges()

    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Submit' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter

    const submit = filteredButtons[0]
    await submit.click()
    fixture.detectChanges()
    
    expect(compiled.textContent).toContain('You must select a quote to include')
  })

  it('should call the service when everything is valid', async () => {
    component.selectedQuotes= [2]
    fixture.detectChanges()

    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Submit' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter
    spyOn(invoiceService, 'updateInvoice').and.callThrough();
    const submit = filteredButtons[0]
    await submit.click()
    fixture.detectChanges()

    expect(invoiceService.updateInvoice).toHaveBeenCalled()
    
    
  });

  it('should convert "1.00" tax to "100" using fixBackendTaxPercentage', () => {
    expect((component as any).fixBackendTaxPercentage("1.00")).toBe("100");
  });

  it('should parse issuance and due dates correctly if not "N/A"', () => {
    const route = TestBed.inject(ActivatedRoute) as any;
    route.queryParams = of({ 
      status: 'created',
      due_date: "2024-10-01",
      issuance_date: "2024-09-01",
      customer: "Alex Guo",
      tax: "0.06"
    });
    route.paramMap = of({ get: () => '5' });

    fixture = TestBed.createComponent(EditInvoicePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    expect(component.range.controls.issued.value?.getFullYear()).toBe(2024);
    expect(component.range.controls.issued.value?.getMonth()).toBe(8); // September
    expect(component.range.controls.issued.value?.getDate()).toBe(1);

    expect(component.range.controls.due.value?.getMonth()).toBe(9); // October
  });

  it('should open confirmation dialog when initial status is issued or paid', () => {
    component.initialStatus = 'issued';
    component.status = 'created';
    component.selectedQuotes = [1];
    component.taxAmount.setValue(10);
    spyOn(component.dialog, 'open').and.callThrough();

    component.openDialog();

    expect(component.dialog.open).toHaveBeenCalled();
  });

  it('setSelectedQuotes should set error flag correctly', () => {
    component.setSelectedQuotes([]);
    expect(component.selectedQuotesIsError).toBeTrue();

    component.setSelectedQuotes([1, 2]);
    expect(component.selectedQuotesIsError).toBeFalse();
  }); 

});
