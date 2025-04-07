import {Component, Input} from '@angular/core';
import {MatDialogActions, MatDialogClose, MatDialogContent, MatDialogTitle} from "@angular/material/dialog";
import {JobDisplayTableComponent} from '../../../components/job-display-table/job-display-table.component';
import {
  MatAccordion,
  MatExpansionPanel,
  MatExpansionPanelHeader,
  MatExpansionPanelTitle
} from '@angular/material/expansion';
import {MatDatepicker, MatDatepickerInput, MatDatepickerToggle} from '@angular/material/datepicker';
import {MatHint, MatInput, MatSuffix} from '@angular/material/input';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  Validators
} from '@angular/forms';
import {MatOption, MatSelect} from '@angular/material/select';
import {MatError, MatFormField} from '@angular/material/form-field';
import {MatButton} from '@angular/material/button';
import {InputFieldDictionary} from '../../../interfaces/interface-helpers/inputField-row-helper.interface';
import {Customer} from '../../../interfaces/customer.interface';
import {Service} from '../../../interfaces/service.interface';
import {Material} from '../../../interfaces/material.interface';
import {Contractor} from '../../../interfaces/contractor.interface';
import {Job} from '../../../interfaces/job.interface';
import {CustomerService} from '../../../services/customer.service';
import {Router} from '@angular/router';
import {ErrorHandlerService} from '../../../services/error.handler.service';
import {ServiceService} from '../../../services/service.service';
import {MaterialService} from '../../../services/material.service';
import {ContractorService} from '../../../services/contractor.service';
import {JobService} from '../../../services/job.service';
import {StringFormatter} from '../../../utils/string-formatter';
import {State, StateList} from '../../../utils/states-list';
import {TableApiResponse} from '../../../interfaces/api-responses/table.api.interface';
import {AddSelectDialogData} from '../../../interfaces/interface-helpers/addSelectDialog-helper.interface';
import {
  AddSelectDialogComponentComponent
} from '../../../components/add-select-dialog-component/add-select-dialog-component.component';

@Component({
  selector: 'app-jobs-helper',
  imports: [
    MatDialogTitle,
    MatDialogActions,
    MatDialogClose,
    JobDisplayTableComponent,
    MatAccordion,
    MatButton,
    MatDatepicker,
    MatDatepickerInput,
    MatDatepickerToggle,
    MatError,
    MatExpansionPanel,
    MatExpansionPanelHeader,
    MatExpansionPanelTitle,
    MatFormField,
    MatHint,
    MatInput,
    MatOption,
    MatSelect,
    MatSuffix,
    ReactiveFormsModule,
    MatDialogContent
  ],
  templateUrl: './jobs-helper.component.html',
  styleUrl: './jobs-helper.component.scss'
})
export class JobsHelperComponent {
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
  selectedCustomers: Customer[] = []
  selectedCustomersIsError = false
  selectedServices: Service[] = []
  selectedServicesIsError = false
  selectedMaterials: Material[] = []
  selectedMaterialsIsError = false
  selectedContractors: Contractor[] = []
  selectedContractorsIsError = false
  materialInputFields: InputFieldDictionary[] = []
  jobForm: FormGroup;
  states: State[]
  job: Job = {
    id: 0,
    jobStatus: 'created',
    startDate: new Date(),
    endDate: new Date(),
    description: '',
    customerName: '',
    customerID: 0,
    jobAddress: '',
    jobCity: '',
    requesterState: '',
    requesterZip: '',
}

  constructor(
    private customerService: CustomerService,
    private router: Router,
    private errorHandler: ErrorHandlerService,
    private serviceService: ServiceService,
    private materialService: MaterialService,
    private contractorService: ContractorService,
    private jobService: JobService,
    private stringFormatter: StringFormatter,
    private jobFormBuilder: FormBuilder,
  ) {
    this.jobForm = this.jobFormBuilder.group({
      requestorAddress: [''],
      requestorCity: [''],
      requestorZip: [''],
      requestorStateSelect: ['', Validators.required],
      jobDescription: ['', Validators.required]
    });

    this.states = StateList
  }

  ngOnInit(): void {
    this.loadCustomersToTable("", 5, 0);
  }


  loadCustomersToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.customers = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  dateValidator(formControl: AbstractControl): ValidationErrors | null {
    const formGroup = formControl as FormGroup;
    const startDate = formGroup?.get('startDate')?.value;
    const endDate = formGroup?.get('endDate')?.value;

    if (!startDate) {
      return { noStartDate: true };
    }

    if (!endDate) {
      return { noEndDate: true };
    }

    return endDate >= startDate ? null : { endDateBefore: true };
  }

  openChangeCustomerDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'customer',
      dialogData: this.customerID,
      searchHint: 'Search by customer name',
      headers: ['First Name','Last Name', 'Email', 'Phone No'],
      materialInputFields: this.materialInputFields,
    };

    const dialogRef = this.dialog.open(AddSelectDialogComponentComponent, {
      width: 'auto',
      maxWidth: '90vw',
      height: 'auto',
      maxHeight: '90vh',
      data: dialogData
    });

    dialogRef.afterClosed().subscribe((result: any) => {
      if (result.length !== 0) {
        const customerEntry = result.itemsInfo[0]
        this.jobForm.controls['customerName'].setValue(customerEntry.first_name + " " + customerEntry.last_name)
        this.customerID = customerEntry.id;
        this.selectedCustomer = customerEntry.id

        this.onChangeUpdateButton()
      }
    })
  }


  loadServicesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.serviceService.getService({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.services = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  loadMaterialsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.materialService.getMaterial({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.materials = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  loadContractorsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.contractorService.getContractor({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.contractors = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

}
