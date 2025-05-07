import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AddSelectDialogComponentComponent } from './add-select-dialog-component.component';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { CommonModule } from '@angular/common';
import { TableComponentComponent } from '../table-component/table-component.component';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';
import { of } from 'rxjs';
import { JobService } from '../../services/job.service';
import { CustomerService } from '../../services/customer.service';
import { ServiceService } from '../../services/service.service';
import { MaterialService } from '../../services/material.service';
import { ContractorService } from '../../services/contractor.service';
import { JobTemplateService } from '../../services/jobTemplate.service';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';

class MockJobService { getExcludedJob = () => of({ data: [] }) }
class MockCustomerService { getExcludedCustomer = () => of({ data: [] }) }
class MockServiceService { getExcludedService = () => of({ data: [] }) }
class MockMaterialService { getExcludedMaterial = () => of({ data: [] }) }
class MockContractorService { getExcludedContractor = () => of({ data: [] }) }
class MockJobTemplateService { getJobTemplate = () => of({ data: [] }) }

describe('AddSelectDialogComponentComponent', () => {
  let component: AddSelectDialogComponentComponent;
  let fixture: ComponentFixture<AddSelectDialogComponentComponent>;
  let mockDialogRef: MatDialogRef<AddSelectDialogComponentComponent>;

  const configureTestBed = (dialogData: any) => {
    TestBed.configureTestingModule({
      imports: [
        CommonModule,
        MatDialogModule,
        MatButtonModule,
        AddSelectDialogComponentComponent,
        TableComponentComponent,    
        LoadingFallbackComponent
      ],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(), 
        { provide: MatDialogRef, useValue: { close: () => {} } },
        { provide: MAT_DIALOG_DATA, useValue: dialogData },
        { provide: JobService, useClass: MockJobService },
        { provide: CustomerService, useClass: MockCustomerService },
        { provide: ServiceService, useClass: MockServiceService },
        { provide: MaterialService, useClass: MockMaterialService },
        { provide: ContractorService, useClass: MockContractorService },
        { provide: JobTemplateService, useClass: MockJobTemplateService },
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AddSelectDialogComponentComponent);
    component = fixture.componentInstance;
    mockDialogRef = TestBed.inject(MatDialogRef);
    fixture.detectChanges();
  };

  it('should create', () => {
    configureTestBed({ typeOfDialog: 'job', dialogData: {} });
    expect(component).toBeTruthy();
  });

  it('should initialize with job data', () => {
    configureTestBed({ 
      typeOfDialog: 'job',
      dialogData: {},
      searchHint: 'Search jobs',
      headers: ['ID', 'Name']
    });
    expect(component.headers).toEqual(['ID', 'Name']);
    expect(component.searchHint).toBe('Search jobs');
  });

  it('should call mockDialogRef.close with false when onCancel is called', () => {
    spyOn(mockDialogRef, 'close');
    component.onCancel();
    expect(mockDialogRef.close).toHaveBeenCalledWith([]);
  });

  it('should handle service selection', () => {
    configureTestBed({
      typeOfDialog: 'service',
      dialogData: { services: [] },
      materialInputFields: []
    });
    
    component.setSelectedServices([1, 2]);
    expect(component.selectedServices).toEqual([1, 2]);
  });

  it('should handle material selection', () => {
    configureTestBed({
      typeOfDialog: 'material',
      dialogData: { materials: [] },
      materialInputFields: []
    });
    
    component.setSelectedMaterials([1, 2]);
    expect(component.selectedMaterials).toEqual([1, 2]);
    expect(component.materialInputFields.length).toBe(2);
  });

  it('should handle contractor selection', () => {
    configureTestBed({
      typeOfDialog: 'contractor',
      dialogData: { contractors: [] },
      materialInputFields: []
    });
    
    component.setSelectedContractors([1, 2]);
    expect(component.selectedContractors).toEqual([1, 2]);
  });

  it('should handle template dialog type', () => {
    configureTestBed({
      typeOfDialog: 'template',
      dialogData: [],
      headers: ['Templates']
    });
    
    expect(component.getButtonAction()).toBe('apply');
  });

  it('should return correct input field values', () => {
    configureTestBed({
      typeOfDialog: 'material',
      dialogData: { materials: [] },
      materialInputFields: [
        { id: 1, unitsUsed: 5, pricePerUnit: 10 }
      ]
    });
    
    expect(component.getUnitsUsedValue(1)).toBe(5);
    expect(component.getPricePerUnitValue(1)).toBe(10);
    expect(component.getUnitsUsedValue(2)).toBe('');
  });

  it('should handle customer selection', () => {
    configureTestBed({
      typeOfDialog: 'customer',
      dialogData: 0,
      headers: ['Customer']
    });
    
    component.setSelectedCustomer([456]);
    expect(component.selectedCustomer).toEqual([456]);
    expect(component.isNotSelectedItems).toBeFalse();
  });

  it('should handle job selection', () => {
    configureTestBed({
      typeOfDialog: 'job',
      dialogData: { jobs: [] },
      materialInputFields: []
    });
    
    component.setSelectedJob([1]);
    expect(component.selectedJob).toEqual([1]);
  });

  it('should handle template selection', () => {
    configureTestBed({
      typeOfDialog: 'template',
      dialogData: { templates: [] },
      materialInputFields: []
    });
    
    component.setSelectedJobTemplate([1]);
    expect(component.selectedTemplate).toEqual([1]);
  });
});