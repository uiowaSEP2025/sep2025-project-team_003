import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { CreateInvoicePageComponent } from './create-invoice-page.component';
import { HttpClient } from '@angular/common/http';
import { HttpHandler } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { MatButtonHarness } from '@angular/material/button/testing';
import { MatSelectHarness } from '@angular/material/select/testing';
import { InvoiceService } from '../../services/invoice.service';
import { HttpTestingController } from '@angular/common/http/testing';

describe('CreateInvoicePageComponent', () => {
  let component: CreateInvoicePageComponent;
  let fixture: ComponentFixture<CreateInvoicePageComponent>;
  let httpMock: HttpTestingController;
  let invoiceService: InvoiceService;

  let loader: HarnessLoader;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateInvoicePageComponent],
      providers: [provideHttpClientTesting(), HttpClient, HttpHandler,
      provideAnimationsAsync()
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(CreateInvoicePageComponent);
    loader = TestbedHarnessEnvironment.loader(fixture);
    component = fixture.componentInstance;
    invoiceService = TestBed.inject(InvoiceService);
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display error when no customer is selected', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Create' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter

    const submit = filteredButtons[0]; // Assuming there's only one "Create" button
    await submit.click()
    fixture.detectChanges()
    expect(compiled.textContent).toContain('You must select a customer to invoice')
  })

  it('should show the second table when a customer is selected', async () => {
    const compiled = fixture.debugElement.nativeElement;
    component.selectedCustomers = [1]
    fixture.detectChanges()
    expect(compiled.querySelectorAll('div[data-testid="app-table"]').length).toEqual(2)
  })

  it('should display date picker when status is not created', async () => {
    const select = (await loader.getAllHarnesses(MatSelectHarness))[1]
    const compiled = fixture.debugElement.nativeElement;
    await select.open();
    const options = await select.getOptions();
    await options[1].click()
    fixture.detectChanges()
    expect(compiled.textContent).toContain("Choose Dates")
  })

  it('should not display date picker when status is created', async () => {
    const compiled = fixture.debugElement.nativeElement;
    fixture.detectChanges()
    expect(compiled.textContent).not.toContain("Choose Dates")
  })

  it('should call validate on the view child', async () => {
    const select = (await loader.getAllHarnesses(MatSelectHarness))[1]
    const compiled = fixture.debugElement.nativeElement;
    await select.open();
    const options = await select.getOptions();
    await options[1].click()
    fixture.detectChanges()
    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Create' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter
    spyOn(component.datePicker, 'validate'); // Spy on the function

    const submit = filteredButtons[0]; // Assuming there's only one "Create" button
    await submit.click()
    fixture.detectChanges()

    expect(component.datePicker.validate).toHaveBeenCalled(); // Verify the call
  })

  it('should show error when no quotes are selected', async () => {
    const compiled = fixture.debugElement.nativeElement;
    component.selectedCustomers = [1]
    fixture.detectChanges()
    expect(compiled.querySelectorAll('div[data-testid="app-table"]').length).toEqual(2)

    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Create' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter

    const submit = filteredButtons[0]
    await submit.click()
    fixture.detectChanges()
    
    expect(compiled.textContent).toContain('You must select a job to include')
  })

  it('should call the service when everything is valid', async () => {
    const compiled = fixture.debugElement.nativeElement;
    component.selectedCustomers = [1]
    component.selectedJobs= [2]
    fixture.detectChanges()

    const filteredButtons = await Promise.all(
      (await loader.getAllHarnesses(MatButtonHarness)).map(async (button) => {
        const text = await button.getText();
        return text === 'Create' ? button : null;
      })
    ).then(results => results.filter(button => button !== null)); // correctly working async filter
    
    const tax = compiled.querySelector('[data-testid="tax-input"]');
    tax.value = 6

    tax.dispatchEvent(new Event('input'));
    
    spyOn(invoiceService, 'createInvoice').and.callThrough();
    const submit = filteredButtons[0]
    await submit.click()
    fixture.detectChanges()

    expect(invoiceService.createInvoice).toHaveBeenCalled()
    
    
   })

});
