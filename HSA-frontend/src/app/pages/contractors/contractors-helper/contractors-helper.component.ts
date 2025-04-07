import {Component, Input, OnInit} from '@angular/core';
import {FormControl, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from '@angular/material/dialog';
import {MatInput, MatLabel} from '@angular/material/input';
import {MatError, MatFormField} from '@angular/material/form-field';
import {MatButton} from '@angular/material/button';
import {GenericFormErrorStateMatcher} from '../../../utils/generic-form-error-state-matcher';
import {ContractorService} from '../../../services/contractor.service';
import {ErrorHandlerService} from '../../../services/error.handler.service';
import {Contractor} from '../../../interfaces/contractor.interface';
import {phoneValidator} from '../../../utils/phone-validator';
import {CreateContractorPageComponent} from '../create-contractors-page/create-contractor-page.component';

@Component({
  selector: 'app-contractors-helper',
  imports: [
    FormsModule,
    MatButton,
    MatDialogActions,
    MatDialogClose,
    MatDialogContent,
    MatError,
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule,
    MatDialogTitle
  ],
  templateUrl: './contractors-helper.component.html',
  styleUrl: './contractors-helper.component.scss'
})
export class ContractorsHelperComponent implements OnInit {
  @Input() crudType: 'Create' | 'Update' = 'Create';
  firstNameControl = new FormControl('', Validators.required)
  lastNameControl = new FormControl('', Validators.required)
  emailControl = new FormControl('', [Validators.email, Validators.required])
  phoneControl = new FormControl('', Validators.required, phoneValidator())
  matcher = new GenericFormErrorStateMatcher()

  private isFormValid() {
    return this.firstNameControl.valid &&
      this.lastNameControl.valid &&
      this.emailControl.valid &&
      this.phoneControl.valid;
  }

  constructor(public dialogRef: MatDialogRef<CreateContractorPageComponent>,
              private contractorService: ContractorService,
              private errorHandler: ErrorHandlerService) {
  }

  @Input() contractor!: Contractor;

  ngOnInit() {
    if (this.crudType === 'Update') {
        this.firstNameControl = new FormControl(this.contractor.firstName, Validators.required)
        this.lastNameControl = new FormControl(this.contractor.lastName, Validators.required)
        this.emailControl = new FormControl(this.contractor.email, [Validators.email, Validators.required])
        this.phoneControl = new FormControl(this.contractor.phone, Validators.required, phoneValidator())
    }
  }

  onSubmit() {
    if (!this.isFormValid()) {
      return
    }

    if (this.crudType === 'Update') {
      const args = {
        id: this.contractor.contractorID,
        first_name: this.firstNameControl.value,
        last_name: this.lastNameControl.value,
        email: this.emailControl.value,
        phone: this.phoneControl.value,
      }
      this.contractorService.editContractor(args).subscribe(
        {
          next: () => {
            this.dialogRef.close();
            window.location.reload();
          },
          error: (error) => {
            this.errorHandler.handleError(error)
          }
        }
      )
    } else {
      const args = {
        id: 0,
        first_name: this.firstNameControl.value,
        last_name: this.lastNameControl.value,
        email: this.emailControl.value,
        phone: this.phoneControl.value,
      }
      this.contractorService.createContractor(args).subscribe(
        {
          next: () => {
            this.dialogRef.close();
            window.location.reload();
          },
          error: (error) => {
            this.errorHandler.handleError(error)
          }
        }
      )
    }

  }
}
