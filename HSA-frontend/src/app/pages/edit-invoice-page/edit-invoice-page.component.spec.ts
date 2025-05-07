import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { EditInvoicePageComponent } from './edit-invoice-page.component';
import { ActivatedRoute, Router } from '@angular/router';
import { Subject, of } from 'rxjs';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatSelectHarness } from '@angular/material/select/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { MatButtonHarness } from '@angular/material/button/testing';
import { MatDialog } from '@angular/material/dialog';
import { InvoiceService } from '../../services/invoice.service';
import { JobService } from '../../services/job.service';
import { StringFormatter } from '../../utils/string-formatter';

describe('EditInvoicePageComponent', () => {
  let component: EditInvoicePageComponent;
  let fixture: ComponentFixture<EditInvoicePageComponent>;
  let loader: HarnessLoader;
  let paramMapSubject: Subject<any>;
  let matDialogSpy: jasmine.SpyObj<MatDialog>;
  let invoiceServiceSpy: jasmine.SpyObj<InvoiceService>;
  let jobServiceSpy: jasmine.SpyObj<JobService>;
  let stringFormatterSpy: jasmine.SpyObj<StringFormatter>;
  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of({
        status: 'created',
        due_date: 'N/A',
        issuance_date: 'N/A',
        customer: 'Alex Guo',
        tax: '0.06',
      })
    };

    await TestBed.configureTestingModule({
      imports: [EditInvoicePageComponent],
      providers: [
        provideAnimationsAsync(),
        HttpClient,
        HttpHandler,
        { provide: ActivatedRoute, useValue: activatedRouteMock },
        { provide: MatDialog, useValue: jasmine.createSpyObj('MatDialog', ['open']) },
        { provide: InvoiceService, useValue: jasmine.createSpyObj('InvoiceService', ['updateInvoice']) },
        { provide: JobService, useValue: jasmine.createSpyObj('JobService', ['getJobsByInvoice']) },
        { provide: StringFormatter, useValue: jasmine.createSpyObj('StringFormatter', ['dateFormatter']) },
        { provide: Router, useValue: jasmine.createSpyObj('Router', ['navigate']) },
      ]
    }).compileComponents();

    matDialogSpy       = TestBed.inject(MatDialog) as any;
    invoiceServiceSpy  = TestBed.inject(InvoiceService) as any;
    jobServiceSpy      = TestBed.inject(JobService) as any;
    stringFormatterSpy = TestBed.inject(StringFormatter) as any;
    routerSpy          = TestBed.inject(Router) as any;

    // stub default behaviors
    invoiceServiceSpy.updateInvoice.and.returnValue(of({} as any));
    jobServiceSpy.getJobsByInvoice.and.returnValue(of({
      data: [{ invoice: 123, id: 5 }, { invoice: 999, id: 6 }]
    } as any));
    stringFormatterSpy.dateFormatter.and.returnValue('2025-05-06');

    fixture = TestBed.createComponent(EditInvoicePageComponent);
    component = fixture.componentInstance;
    loader = TestbedHarnessEnvironment.loader(fixture);

    // emit route param so invoiceID is set
    paramMapSubject.next({ get: (_: string) => '123' });
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display date picker when status is not created', async () => {
    const select = (await loader.getAllHarnesses(MatSelectHarness))[0];
    const compiled = fixture.debugElement.nativeElement;

    await select.open();
    const options = await select.getOptions();
    await options[2].click();
    fixture.detectChanges();

    expect(compiled.textContent).toContain('Choose Dates');
  });

  it('should not display date picker when status is created', async () => {
    const compiled = fixture.debugElement.nativeElement;
    fixture.detectChanges();
    expect(compiled.textContent).not.toContain('Choose Dates');
  });

  it('should call validate on the view child', async () => {
    const select = (await loader.getAllHarnesses(MatSelectHarness))[0];
    await select.open();
    const options = await select.getOptions();
    await options[1].click();
    fixture.detectChanges();

    spyOn(component.datePicker, 'validate');

    const buttons = await loader.getAllHarnesses(MatButtonHarness);
    const submit = (await Promise.all(buttons.map(async b => {
      const text = await b.getText();
      return text === 'Submit' ? b : null;
    }))).find(b => b !== null)!;

    await submit.click();
    fixture.detectChanges();

    expect(component.datePicker.validate).toHaveBeenCalled();
  });

  it('should show error when no quotes are selected', async () => {
    const compiled = fixture.debugElement.nativeElement;
    fixture.detectChanges();

    const buttons = await loader.getAllHarnesses(MatButtonHarness);
    const submit = (await Promise.all(buttons.map(async b => {
      const text = await b.getText();
      return text === 'Submit' ? b : null;
    }))).find(b => b !== null)!;

    await submit.click();
    fixture.detectChanges();

    expect(compiled.textContent).toContain('You must select a job to include');
  });

  it('should call the service when everything is valid', async () => {
    component.selectedJobs = [2];
    fixture.detectChanges();

    const buttons = await loader.getAllHarnesses(MatButtonHarness);
    const submit = (await Promise.all(buttons.map(async b => {
      const text = await b.getText();
      return text === 'Submit' ? b : null;
    }))).find(b => b !== null)!;

    // spyOn(invoiceServiceSpy, 'updateInvoice').and.callThrough();
    await submit.click();
    fixture.detectChanges();

    expect(invoiceServiceSpy.updateInvoice).toHaveBeenCalled();
  });

  it('setSelectedJobs toggles error correctly', () => {
    component.setSelectedJobs([]);
    expect(component.selectedJobsisError).toBeTrue();

    component.setSelectedJobs([1, 2]);
    expect(component.selectedJobsisError).toBeFalse();
  });

  it('loadJobs populates jobs & selectedJobs on first load', () => {
    component.loadJobs('', 5, 0);

    expect(component.jobs.data.length).toBe(2);
    expect(component.isFirstLoad).toBeFalse();

    component.selectedJobs = [99];
    component.loadJobs('', 5, 0);
    expect(component.selectedJobs).toEqual([99]);
  });

  it('openDialog calls updateInvoice and navigates when result=true', () => {
    component.initialStatus = 'issued';
    component.status = 'issued';
    component.selectedJobs = [42];
    component.range.controls.issued.setValue(new Date(2025, 0, 1));
    component.range.controls.due.setValue(new Date(2025, 0, 2));

    matDialogSpy.open.and.returnValue({ afterClosed: () => of(true) } as any);

    component.openDialog();

    expect(routerSpy.navigate).toHaveBeenCalledWith(['/invoices']);
  });

  it('onSubmit valid path calls updateInvoice & navigate', () => {
    component.initialStatus = 'created';
    component.status = 'created';
    component.selectedJobs = [77];
    component.range.controls.issued.setValue(new Date());
    component.range.controls.due.setValue(new Date());

    component.onSubmit();

    expect(invoiceServiceSpy.updateInvoice).toHaveBeenCalled();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/invoices']);
  });
});
