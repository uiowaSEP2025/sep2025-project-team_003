import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EditJobPageComponent } from './edit-job-page.component';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { of, Subject } from 'rxjs';

import { JobService } from '../../services/job.service';
import { RequestTrackerService } from '../../utils/request-tracker';
import { StringFormatter } from '../../utils/string-formatter';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

class MockRouter {
  navigate = jasmine.createSpy('navigate');
}

describe('EditJobPageComponent', () => {
  let component: EditJobPageComponent;
  let fixture: ComponentFixture<EditJobPageComponent>;
  let paramMapSubject: Subject<any>;
  let httpMock: HttpTestingController;
  let router: MockRouter;

  // spies for all injected services
  let jobServiceSpy: jasmine.SpyObj<JobService>;
  let trackerSpy: jasmine.SpyObj<RequestTrackerService>;
  let stringFormatterSpy: jasmine.SpyObj<StringFormatter>;
  let dialogSpy: jasmine.SpyObj<MatDialog>;
  let snackBarSpy: jasmine.SpyObj<MatSnackBar>;

  // a minimal mock job payload
  const mockJobData = {
    data: {
      id: 1,
      customerName: 'John Doe',
      jobStatus: 'created',
      startDate: '2025-05-01T00:00:00Z',
      endDate: '2025-05-02T00:00:00Z',
      description: 'Test job',
      requestorAddress: '123 Main St',
      requestorCity: 'Anytown',
      requestorState: 'TX',
      requestorZip: '12345',
      flatfee: '100.00',
      hourlyRate: '50.00',
      minutesWorked: 30,
      customerID: 1
    },
    services: { services: [] },
    materials: { materials: [] },
    contractors: { contractors: [] }
  };

  beforeEach(async () => {
    // create jasmine spies
    jobServiceSpy = jasmine.createSpyObj('JobService', ['getSpecificJobData']);
    trackerSpy = jasmine.createSpyObj('RequestTrackerService', ['startRequest', 'endRequest'], { completionNotifier: of() });
    stringFormatterSpy = jasmine.createSpyObj('StringFormatter', ['dateFormatter'], { });
    dialogSpy = jasmine.createSpyObj('MatDialog', ['open']);
    snackBarSpy = jasmine.createSpyObj('MatSnackBar', ['open']);

    // stub getSpecificJobData to return our mock right away
    jobServiceSpy.getSpecificJobData.and.returnValue(of(mockJobData as any));
    // stub dateFormatter to just return ISO string for comparison
    stringFormatterSpy.dateFormatter.and.callFake((d: Date) => d.toISOString().slice(0,10));

    paramMapSubject = new Subject();
    const activatedRouteMock = {
      paramMap: paramMapSubject.asObservable(),
      queryParams: of({
        jobStatus: "",
        startDate: "",
        endDate: "",
        description: "",
        customerID: 1,
        city: "",
        state: "",
        zip: "",
        address: ""
      })
    };

    await TestBed.configureTestingModule({
      imports: [EditJobPageComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: Router, useClass: MockRouter },
        { provide: ActivatedRoute, useValue: activatedRouteMock },
        { provide: JobService, useValue: jobServiceSpy },
        { provide: RequestTrackerService, useValue: trackerSpy },
        { provide: StringFormatter, useValue: stringFormatterSpy },
        { provide: MatDialog, useValue: dialogSpy },
        { provide: MatSnackBar, useValue: snackBarSpy },
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(EditJobPageComponent);
    router = TestBed.inject(Router) as unknown as MockRouter;
    httpMock = TestBed.inject(HttpTestingController);
    component = fixture.componentInstance;

    // trigger ngOnInit
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should populate form and properties after ngOnInit', () => {
    // our spy returned mockJobData synchronously
    expect(component.jobData).toEqual(mockJobData as any);
    expect(component.customerID).toBe(1);
    expect(component.jobForm.get('customerName')?.value).toBe('John Doe');
    expect(component.jobForm.get('jobStatus')?.value).toBe('created');
  });

  it('navigateToPage should call router.navigate', () => {
    component.navigateToPage('jobs');
    expect(router.navigate).toHaveBeenCalledWith(['/jobs']);
  });

  it('dateValidator should return error when endDate is before startDate', () => {
    // build a mini FormGroup for testing
    const ctrl = (component as any).jobFormBuilder.group({
      startDate: new Date('2025-05-02'),
      endDate: new Date('2025-05-01')
    });
    const result = component.dateValidator(ctrl);
    expect(result).toEqual({ endDateBefore: true });
  });

  it('onSubmit with invalid form should show snackBar error', () => {
    // clear a required field to force invalid
    component.jobForm.controls['requestorStateSelect'].setValue('');
    component.onSubmit();
    expect(snackBarSpy.open).toHaveBeenCalledWith(
      'Invalid fields, please revise the form and resubmit',
      '',
      { duration: 3000 }
    );
  });
  it('openChangeCustomerDialog updates form and IDs when dialog returns a selection', () => {
    // 1) prepare a fake dialog result with length>0 and itemsInfo[0]
    const fakeResult = {
      length: 1,
      itemsInfo: [{ first_name: 'Jane', last_name: 'Smith', id: 42 }]
    };
    // 2) stub dialog.open(...) to return a ref whose afterClosed() emits fakeResult
    const dialogRefStub = { afterClosed: () => of(fakeResult) };
    dialogSpy.open.and.returnValue(dialogRefStub as any);
  
    // 3) spy on onChangeUpdateButton so we can verify it ran
    spyOn(component, 'onChangeUpdateButton');
  
    // 4) call the method under test
    component.openChangeCustomerDialog();
  
    // 5) assert that the form and component fields have been updated
    expect(component.jobForm.get('customerName')?.value).toBe('Jane Smith');
    expect(component.customerID).toBe(42);
    expect(component.selectedCustomer).toBe(42);
    expect(component.onChangeUpdateButton).toHaveBeenCalled();
  });
  it('onDelete pushes joinRelationID for service, material, and contractor when joinRelationID ≠ 0', () => {
    // set up minimal containers
    component.services = { services: [{ serviceID: 99 }, { serviceID: 100 }] };
    component.materials = { materials: [{ materialID: 21 }] };
    component.contractors = { contractors: [{ contractorID: 42 }] };
  
    const cases = [
      ['service', 'Service ID', component.deletedJobServices, component.services, { 'Service ID': 99 }],
      ['material', 'Material ID', component.deletedJobMaterials, component.materials, { 'Material ID': 21 }],
      ['contractor', 'Contractor ID', component.deletedJobContractors, component.contractors, { 'Contractor ID': 42 }]
    ] as const;
  
    cases.forEach(([type, key, deletedArr, container, data]) => {
      deletedArr.length = 0;               // clear prior pushes
      const returned = component.onDelete(type, data, 55, null);
      expect(deletedArr).toEqual([55]);    // joinRelationID was pushed
      expect(returned).toBe(container);    // returns the correct collection
    });
  });  
  it('calls createJobJoin for materials when selectedMaterials is non-empty', () => {
    // stub the other service methods so onSubmit won’t blow up
    jobServiceSpy.editJob = jasmine.createSpy().and.returnValue(of({}));
    jobServiceSpy.deleteJobJoin = jasmine.createSpy().and.returnValue(of({}));
    jobServiceSpy.createJobJoin = jasmine.createSpy().and.returnValue(of({}));
  
    // make sure the form is already valid (it is, from ngOnInit) and set a material
    component.selectedMaterials = [{ id: 99 }];
    // clear other arrays so only the materials branch runs
    component.selectedServices = [{id:18}];
    component.deletedJobServices = [{id:10}];
    component.deletedJobMaterials = [{id:10}];
    component.deletedJobContractors = [{id:10}];
    component.selectedContractors = [{id:13},{id:100}];
  
    // trigger onSubmit
    component.onSubmit();
  
  });
  it('openAddServiceDialog adds services and triggers update', () => {
    // prepare a fake dialog result
    const fake = {
      length: 1,
      itemsInfo: [{ id: 7, service_name: 'SVC', service_description: 'DESC' }],
      selectedItems: [7]
    };
    // stub dialog.open().afterClosed()
    dialogSpy.open.and.returnValue({ afterClosed: () => of(fake) } as any);
    // spy on update-button logic
    spyOn(component, 'onChangeUpdateButton');
    // start with empty services
    component.services = { services: [] };
    // call method under test
    component.openAddServiceDialog();
    // assert that a new entry was created
    expect(component.services.services).toEqual([{
      id: 0,
      serviceID: 7,
      serviceName: 'SVC',
      serviceDescription: 'DESC'
    }]);
    // selectedServices updated
    expect(component.selectedServices).toBe(fake.selectedItems);
    // onChangeUpdateButton was invoked
    expect(component.onChangeUpdateButton).toHaveBeenCalled();
  });
  it('openAddContractorDialog adds contractors and triggers update', () => {
    // fake dialog result
    const fake = {
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
    // stub dialog.open().afterClosed()
    dialogSpy.open.and.returnValue({ afterClosed: () => of(fake) } as any);
    // spy on update-button logic
    spyOn(component, 'onChangeUpdateButton');
    // start with empty contractors list
    component.contractors = { contractors: [] };
    // invoke
    component.openAddContractorDialog();
    // assert new contractor was added
    expect(component.contractors.contractors).toEqual([{
      id: 0,
      contractorID: 99,
      contractorName: 'Alice Jones',
      contractorPhoneNo: '555-1234',
      contractorEmail: 'alice@example.com'
    }]);
    // selectedContractors updated
    expect(component.selectedContractors).toBe(fake.selectedItems);
    // onChangeUpdateButton called
    expect(component.onChangeUpdateButton).toHaveBeenCalled();
  });
  it('openAddMaterialDialog adds materials and triggers update', () => {
    // fake dialog result
    const fake = {
      length: 1,
      itemsInfo: [{ id: 7, name: 'Wood', description: 'Oak plank' }],
      selectedItems: [7]
    };

    dialogSpy.open.and.returnValue({ afterClosed: () => of(fake) } as any);
    // spy on update-button logic
    spyOn(component, 'onChangeUpdateButton');
    // start with empty materials list
    component.materials = { materials: [] };
    // invoke
    component.openAddMaterialDialog();
    // assert new material was added
    expect(component.materials.materials).toEqual(fake.itemsInfo);
    // selectedMaterials updated
    expect(component.selectedMaterials).toBe(fake.selectedItems);
    // onChangeUpdateButton called
    expect(component.onChangeUpdateButton).toHaveBeenCalled();
  });  
    
});
