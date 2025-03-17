import { ComponentFixture, TestBed } from '@angular/core/testing';
import { InvoiceStateRegressionConfirmerComponent } from './invoice-state-regression-confirmer.component';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogTitle, MatDialogContent, MatDialogActions } from '@angular/material/dialog';

describe('InvoiceStateRegressionConfirmerComponent', () => {
  let component: InvoiceStateRegressionConfirmerComponent;
  let fixture: ComponentFixture<InvoiceStateRegressionConfirmerComponent>;
  let mockDialogRef: jasmine.SpyObj<MatDialogRef<InvoiceStateRegressionConfirmerComponent>>;

  beforeEach(async () => {
    // Create a spy object for MatDialogRef
    mockDialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);

    await TestBed.configureTestingModule({
      imports: [
        InvoiceStateRegressionConfirmerComponent,
        MatFormFieldModule,
        MatInputModule,
        FormsModule,
        MatButtonModule,
        MatDialogTitle,
        MatDialogContent,
        MatDialogActions,
      ],
      providers: [
        { provide: MAT_DIALOG_DATA, useValue: 'created' },
        { provide: MatDialogRef, useValue: mockDialogRef }, // Provide the mock MatDialogRef
      ],
    }).compileComponents();

    // Create the component fixture
    fixture = TestBed.createComponent(InvoiceStateRegressionConfirmerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges(); // Trigger initial data binding
  });

  // Test 1: Ensure the component is created successfully
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // Test 2: Ensure the dialog closes with `false` when `onNoClick` is called
  it('should close dialog with false on onNoClick', () => {
    component.onNoClick(); // Call the method
    expect(mockDialogRef.close).toHaveBeenCalledWith(false); // Verify dialog is closed with `false`
  });

  // Test 3: Ensure the dialog closes with `true` when `onConfirm` is called
  it('should close dialog with true on onConfirm', () => {
    component.onConfirm(); // Call the method
    expect(mockDialogRef.close).toHaveBeenCalledWith(true); // Verify dialog is closed with `true`
  });

  // Test 4: Ensure the correct status is injected via MAT_DIALOG_DATA
  it('should have the correct status injected', () => {
    expect(component.status).toBe('created'); // Verify the injected status matches the mock data
  });

  // Optional: Test with different status values
  describe('with different status values', () => {
    beforeEach(() => {
      // Reset the TestBed before each test in this describe block
      TestBed.resetTestingModule();
      
      TestBed.configureTestingModule({
        imports: [
          InvoiceStateRegressionConfirmerComponent,
          MatFormFieldModule,
          MatInputModule,
          FormsModule,
          MatButtonModule,
          MatDialogTitle,
          MatDialogContent,
          MatDialogActions,
        ],
        providers: [
          { provide: MatDialogRef, useValue: mockDialogRef }, // Provide the mock MatDialogRef
          { provide: MAT_DIALOG_DATA, useValue: {} }, // Provide a default value for MAT_DIALOG_DATA
        ],
      }).compileComponents();
  
    });
  
    it('should handle status "issued"', () => {
      // Override the provider for MAT_DIALOG_DATA before fixture creation or detection
      TestBed.overrideProvider(MAT_DIALOG_DATA, { useValue: 'issued' });
      fixture = TestBed.createComponent(InvoiceStateRegressionConfirmerComponent);
      component = fixture.componentInstance;
      // Detect changes after overriding
      fixture.detectChanges();
      const compiled = fixture.debugElement.nativeElement;
  
      // Verify the new status
      expect(component.status).toBe('issued');
      expect(compiled.textContent).toContain('The invoice was already issued to the customer.')
    });
  
    it('should handle status "paid"', () => {
      // Override the provider for MAT_DIALOG_DATA before fixture creation or detection
      TestBed.overrideProvider(MAT_DIALOG_DATA, { useValue: 'paid' });
      fixture = TestBed.createComponent(InvoiceStateRegressionConfirmerComponent);
      component = fixture.componentInstance;
      // Detect changes after overriding
      fixture.detectChanges();
      const compiled = fixture.debugElement.nativeElement;
      // Verify the new status
      expect(component.status).toBe('paid');
      expect(compiled.textContent).toContain('The customer has already paid for this invoice')
    });
  });
  
});