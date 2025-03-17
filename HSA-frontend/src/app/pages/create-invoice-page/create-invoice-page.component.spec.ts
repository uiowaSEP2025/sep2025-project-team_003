import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { CreateInvoicePageComponent } from './create-invoice-page.component';
import { HttpClient } from '@angular/common/http';
import { HttpHandler } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { MatButtonHarness } from '@angular/material/button/testing';

fdescribe('CreateInvoicePageComponent', () => {
  let component: CreateInvoicePageComponent;
  let fixture: ComponentFixture<CreateInvoicePageComponent>;
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

  fit('should show the second table when a customer is selected', async () => { 
    const compiled = fixture.debugElement.nativeElement;
    component.selectedCustomers = [1]
    fixture.detectChanges()
    expect(compiled.querySelectorAll('table').length).toEqual(2)

  })

  it('should display date picker when status is not created', () => { })

  it('should call validate on the view child', () => { })

  it('should show error when no quotes are selected', () => { })

  it('should call the endpoint when everything is valid', () => { })

});
