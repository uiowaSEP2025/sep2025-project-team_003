import {Component, Input, OnInit} from '@angular/core';
import {
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatInput} from '@angular/material/input';
import {
  FormBuilder, FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import {MatFormField, MatLabel} from '@angular/material/form-field';
import {MatButton} from '@angular/material/button';
import {InputFieldDictionary} from '../../../interfaces/interface-helpers/inputField-row-helper.interface';
import {Customer} from '../../../interfaces/customer.interface';
import {Service} from '../../../interfaces/service.interface';
import {Material} from '../../../interfaces/material.interface';
import {Contractor} from '../../../interfaces/contractor.interface';
import {Job} from '../../../interfaces/job.interface';
import {CustomerService} from '../../../services/customer.service';
import {ErrorHandlerService} from '../../../services/error.handler.service';
import {ServiceService} from '../../../services/service.service';
import {MaterialService} from '../../../services/material.service';
import {ContractorService} from '../../../services/contractor.service';
import {State, StateList} from '../../../utils/states-list';
import {TableApiResponse} from '../../../interfaces/api-responses/table.api.interface';
import {CreateJobPageComponent} from '../create-job-page/create-job-page.component';
import {JobService} from '../../../services/job.service';

@Component({
  selector: 'app-jobs-helper',
  imports: [
    MatDialogTitle,
    MatDialogActions,
    MatDialogClose,
    MatButton,
    MatFormField,
    MatInput,
    ReactiveFormsModule,
    MatDialogContent,
    MatLabel
  ],
  templateUrl: './jobs-helper.component.html',
  styleUrl: './jobs-helper.component.scss'
})
export class JobsHelperComponent implements OnInit {
  @Input() crudType: 'Create' | 'Update' = 'Create';
  customers: TableApiResponse<Customer> = {
    data: [],
    totalCount: 0
  }
  services: TableApiResponse<Service> = {
    data: [],
    totalCount: 0
  }
  materials: TableApiResponse<Material> = {
    data: [],
    totalCount: 0
  }
  contractors: TableApiResponse<Contractor> = {
    data: [],
    totalCount: 0
  }
  materialInputFields: InputFieldDictionary[] = []
  jobForm: FormGroup;
  states: State[]
  @Input() job!: Job;

  constructor(
    public dialogRef: MatDialogRef<CreateJobPageComponent>,
    private customerService: CustomerService,
    private errorHandler: ErrorHandlerService,
    private serviceService: ServiceService,
    private materialService: MaterialService,
    private contractorService: ContractorService,
    private jobService: JobService,
    private jobFormBuilder: FormBuilder,
  ) {
    this.jobForm = this.jobFormBuilder.group({
      jobStatus: new FormControl('', Validators.required),
      jobStartDate: new FormControl('', [Validators.required]),
      jobEndDate: new FormControl('', [Validators.required]),
      jobAddress: new FormControl(['']),
      jobCity: new FormControl(['']),
      jobZip: new FormControl(['']),
      jobStateSelect: new FormControl(['', Validators.required]),
      jobDescription: new FormControl(['', Validators.required]),
      jobMaterials: new FormControl([[]]),
      jobServices: new FormControl([[], Validators.required]),
      jobCustomer: new FormControl([{
        customerID: 0,
        customerName: '',
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
      }, Validators.required]),
    });

    this.states = StateList
  }

  ngOnInit(): void {
    if (this.crudType === 'Update') {

      this.jobForm.setValue(
        {
          jobStatus: this.job.jobStatus,
          jobStartDate: this.job.startDate,
          jobEndDate: this.job.endDate,
          jobDescription: this.job.description,
          jobMaterials: this.job.materials,
          jobServices: this.job.services,
          jobAddress: this.job.jobAddress,
          jobCity: this.job.jobCity,
          jobZip: this.job.jobZip,
          jobStateSelect: this.job.jobState,
          jobCustomer: this.job.customer,
        }
      )
    }
  }


  onSubmit() {

  }
}
