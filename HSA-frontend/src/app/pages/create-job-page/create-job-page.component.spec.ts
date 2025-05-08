import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CreateJobPageComponent } from './create-job-page.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { of, Subject } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { JobService } from '../../services/job.service';
import { JobTemplateService } from '../../services/jobTemplate.service';
import { StringFormatter } from '../../utils/string-formatter';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('CreateJobPageComponent', () => {
  let component: CreateJobPageComponent;
  let fixture: ComponentFixture<CreateJobPageComponent>;
  let httpMock: HttpTestingController;
  let router: MockRouter;
  let paramMapSubject: Subject<any>;
  let matDialogSpy: jasmine.SpyObj<MatDialog>;
  let snackBarSpy: jasmine.SpyObj<MatSnackBar>;
  let mockJobService: jasmine.SpyObj<JobService>;
  let mockJobTemplateService: jasmine.SpyObj<JobTemplateService>;
  let mockStringFormatter: jasmine.SpyObj<StringFormatter>;

  beforeEach(async () => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of({
        jobStatus: '', startDate: '', endDate: '', description: '',
        customerID: 1, city: '', state: '', zip: '', address: ''
      })
    };

    matDialogSpy = jasmine.createSpyObj('MatDialog', ['open']);
    snackBarSpy = jasmine.createSpyObj('MatSnackBar', ['open']);

    mockJobService           = jasmine.createSpyObj('JobService', ['createJob']);
    mockJobService.createJob.and.returnValue(of({} as any));
    mockJobTemplateService   = jasmine.createSpyObj('JobTemplateService', ['createJobTemplate']);
    mockJobTemplateService.createJobTemplate.and.returnValue(of({} as any));
    mockStringFormatter      = jasmine.createSpyObj('StringFormatter', ['dateFormatter']);
    mockStringFormatter.dateFormatter.and.returnValue('2025-05-06');

    // default for all non-template opens (e.g. service/material dialogs)
    const fakeAddRef = {
      afterClosed: () => of({
        length: 1,
        itemsInfo: [{ id: 42, service_name: 'Svc', service_description: 'Desc' }],
        selectedItems: ['svc']
      })
    };
    matDialogSpy.open.and.returnValue(fakeAddRef as any);

    await TestBed.configureTestingModule({
      imports: [CreateJobPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: Router, useClass: MockRouter },
        { provide: ActivatedRoute, useValue: activatedRouteMock },
        { provide: MatDialog, useValue: matDialogSpy },
        { provide: MatSnackBar, useValue: snackBarSpy },
        { provide: JobService, useValue: mockJobService },
        { provide: JobTemplateService, useValue: mockJobTemplateService },
        { provide: StringFormatter, useValue: mockStringFormatter },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(CreateJobPageComponent);
    router  = TestBed.inject(Router) as any;
    httpMock = TestBed.inject(HttpTestingController);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('navigateToPage should call router.navigate', () => {
    component.navigateToPage('jobs');
    expect(router.navigate).toHaveBeenCalledWith(['/jobs']);
  });

  it('dateValidator returns noStartDate when startDate is missing', () => {
    const fakeGroup: any = {
      get: (key: string) => ({ value: key === 'startDate' ? null : new Date() })
    };
    expect(component.dateValidator(fakeGroup as any)).toEqual({ noStartDate: true });
  });

  it('openAddServiceDialog updates services & flags', () => {
    component.services = { services: [] };
    component.openAddServiceDialog();
    expect(component.services.services.length).toBe(1);
    expect(component.selectedServices).toEqual(['svc']);
    expect(component.isUpdatedField).toBeTrue();
  });

  it('onDelete for service removes it when joinRelationID is 0', () => {
    component.services = { services: [{ serviceID: 42 }] };
    component.selectedServices = ['svc'];
    const result = component.onDelete('service', { 'Service ID': 42 }, 0, 'svc');
    expect(result.services).toEqual([]);
    expect(component.selectedServices.length).toBe(0);
  });

  it('onSubmit calls createJob & navigates on valid form', () => {
    component.jobForm.patchValue({
      customerName: 'Test', startDate: new Date(), endDate: new Date(),
      requestorAddress: 'A', requestorCity: 'B', requestorZip: 'C',
      requestorStateSelect: 'D', jobDescription: 'desc',
      flatfee: '0.00', hourlyRate: '0.00', minutesWorked: '0'
    });
    component.selectedCustomer = 1;
    component.onSubmit();
    expect(mockJobService.createJob).toHaveBeenCalled();
    expect(snackBarSpy.open)
      .toHaveBeenCalledWith('Job create successfully', '', { duration: 3000 });
    expect(router.navigate).toHaveBeenCalledWith(['/jobs']);
  });

  it('onCreateConfirmDialog("template") uses template service and snackbar', () => {
    // override dialog.open to return a template-shaped result
    const templateResult = {
      description: 'desc',
      name: 'T1',
      services: { services: [{ serviceID: 123 }] },
      materials: { materials: [{ materialID: 456, unitsUsed: 2, pricePerUnit: 9 }] }
    };
    const fakeTemplateRef = { afterClosed: () => of(templateResult) };
    matDialogSpy.open.and.returnValue(fakeTemplateRef as any);

    component.jobForm.patchValue({ jobDescription: 'desc' });
    component.onCreateConfirmDialog('template');

    expect(mockJobTemplateService.createJobTemplate as any).toHaveBeenCalledWith({
      description: 'desc',
      name:        'T1',
      services:    [{ id: 123 }],
      materials:   [{ id: 456, unitsUsed: 2, pricePerUnit: 9 }]
    });
    expect(snackBarSpy.open)
      .toHaveBeenCalledWith('Job template create successfully', '', { duration: 3000 });
  });

  it('openApplyTemplateDialog applies template and updates fields', () => {
    // prepare a fake template payload
    const fakeTemplate = {
      jobDescription: 'TemplateDesc',
      services:  { services: [{ serviceID: 5, foo: 'bar' }] },
      materials: { materials: [{ materialID: 7, qty: 2 }] }
    };
    const fakeResult = {
      length: 1,
      selectedItems: [ fakeTemplate ]
    };
  
    // stub dialog.open().afterClosed()
    matDialogSpy.open.and.returnValue({
      afterClosed: () => of(fakeResult)
    } as any);
  
    // spy on onChangeUpdateButton
    spyOn(component, 'onChangeUpdateButton');
  
    // reset services/materials
    component.services  = { services: [] };
    component.materials = { materials: [] };
  
    // call method
    component.openApplyTemplateDialog();
  
    // assertions
    expect(component.jobForm.get('jobDescription')!.value).toBe('TemplateDesc');
    expect(component.services.services).toEqual(fakeTemplate.services.services);
    expect(component.selectedServices).toBe(fakeResult.selectedItems);
    expect(component.materials.materials).toEqual(fakeTemplate.materials.materials);
    expect(component.selectedMaterials).toBe(fakeResult.selectedItems);
    expect(component.onChangeUpdateButton).toHaveBeenCalled();
    expect(snackBarSpy.open)
      .toHaveBeenCalledWith('Job template applied successfully', '', { duration: 3000 });
    expect(component.isAllowedTemplate).toBeFalse();
  });
  it('openAddContractorDialog adds contractors & triggers update', () => {
    const fakeResult = {
      length: 1,
      itemsInfo: [{
        id: 99,
        first_name: 'Alice',
        last_name: 'Jones',
        phone: '555-1234',
        email: 'alice@example.com'
      }],
      selectedItems: [99]
    };
  
    matDialogSpy.open.and.returnValue({
      afterClosed: () => of(fakeResult)
    } as any);
  
    spyOn(component, 'onChangeUpdateButton');
    component.contractors = { contractors: [] };
  
    component.openAddContractorDialog();
  
    expect(component.contractors.contractors).toEqual([{
      id: 0,
      contractorID: 99,
      contractorName: 'Alice Jones',
      contractorPhoneNo: '555-1234',
      contractorEmail: 'alice@example.com'
    }]);
    expect(component.selectedContractors).toBe(fakeResult.selectedItems);
    expect(component.onChangeUpdateButton).toHaveBeenCalled();
  });
  it('onDelete("service",…) removes the service and updates state when joinRelationID is 0', () => {
  spyOn(component, 'onChangeUpdateButton');
  // start with two services and two selected items
  component.services = { services: [{ serviceID: 1 }, { serviceID: 2 }] };
  component.selectedServices = ['sel1', 'sel2'];

  const result = component.onDelete(
    'service',
    { 'Service ID': 1 },
    99,
    'sel1'
  );

  // serviceID 1 should be gone
  expect(result.services).toEqual([{ serviceID: 2 }]);
  expect(component.onChangeUpdateButton).toHaveBeenCalled();
});



it('openAddCustomerDialog sets customerName, customerID, selectedCustomer and triggers update', () => {
  const fakeResult = {
    length: 1,
    itemsInfo: [{
      id: 7,
      first_name: 'Bob',
      last_name: 'Smith',
      email: 'bob@example.com',
      phone: '123-4567'
    }],
    selectedItems: [7]
  };

  matDialogSpy.open.and.returnValue({ afterClosed: () => of(fakeResult) } as any);
  spyOn(component, 'onChangeUpdateButton');

  component.jobForm.controls['customerName'].setValue('');
  component.customerID = 0;
  component.selectedCustomer = 0;

  component.openAddCustomerDialog();

  expect(component.jobForm.controls['customerName'].value).toBe('Bob Smith');
  expect(component.customerID).toBe(7);
  expect(component.selectedCustomer).toBe(7);
  expect(component.onChangeUpdateButton).toHaveBeenCalled();
});
it('openAddMaterialDialog adds materials & triggers update', () => {
  const fakeResult = {
    length: 1,
    itemsInfo: [{
      materialID: 11,
      materialName: 'Wood',
      materialDescription: 'Oak'
    }],
    selectedItems: [11]
  };

  matDialogSpy.open.and.returnValue({ afterClosed: () => of(fakeResult) } as any);
  spyOn(component, 'onChangeUpdateButton');

  component.materials = { materials: [] };

  component.openAddMaterialDialog();

  expect(component.materials.materials).toEqual(fakeResult.itemsInfo);
  expect(component.selectedMaterials).toBe(fakeResult.selectedItems);
  expect(component.onChangeUpdateButton).toHaveBeenCalled();
});

  
});
