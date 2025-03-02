import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DeleteDialogComponentComponent } from './delete-dialog-component.component';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { StringFormatter } from '../../utils/string-formatter';

describe('DeleteDialogComponentComponent', () => {
  let component: DeleteDialogComponentComponent;
  let fixture: ComponentFixture<DeleteDialogComponentComponent>;
  let mockDialogRef: jasmine.SpyObj<MatDialogRef<DeleteDialogComponentComponent>>;
  let mockStringFormatter: jasmine.SpyObj<StringFormatter>;

  beforeEach(async () => {
    mockDialogRef = jasmine.createSpyObj('MatDialogRef', ['close']);
    mockStringFormatter = jasmine.createSpyObj('StringFormatter', ['formatJSONData']);

    await TestBed.configureTestingModule({
      imports: [DeleteDialogComponentComponent],
      providers: [
        { provide: MatDialogRef, useValue: mockDialogRef },
        { provide: MAT_DIALOG_DATA, useValue: {} },
        { provide: StringFormatter, useValue: mockStringFormatter }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DeleteDialogComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call dialogRef.close with false when onCancel is called', () => {
    component.onCancel();
    expect(mockDialogRef.close).toHaveBeenCalledWith(false);
  });

  it('should call dialogRef.close with true when onConfirm is called', () => {
    component.onConfirm();
    expect(mockDialogRef.close).toHaveBeenCalledWith(true);
  });
});