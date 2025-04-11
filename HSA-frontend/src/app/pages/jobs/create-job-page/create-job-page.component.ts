import { Component, OnInit, ViewChild } from '@angular/core';
import { InvoiceDatePickerComponent } from '../../../components/invoice-date-picker/invoice-date-picker.component';
import { CustomerService } from '../../../services/customer.service';
import { Router } from '@angular/router';
import { StringFormatter } from '../../../utils/string-formatter';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { TableComponentComponent } from '../../../components/table-component/table-component.component';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatError, MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { LoadingFallbackComponent } from "../../../components/loading-fallback/loading-fallback.component";
import { ServiceService } from '../../../services/service.service';
import { MaterialService } from '../../../services/material.service';
import { ContractorService } from '../../../services/contractor.service';
import { InputFieldDictionary } from '../../../interfaces/interface-helpers/inputField-row-helper.interface';
import { DateRange } from '../../invoices/edit-invoice-page/edit-invoice-page.component';
import { JobService } from '../../../services/job.service';
import { StateList } from '../../../utils/states-list';
import {JobsHelperComponent} from '../jobs-helper/jobs-helper.component';



@Component({
  selector: 'app-create-job-page',
  imports: [
    CommonModule,
    MatButtonModule,
    FormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    JobsHelperComponent
  ],
  templateUrl: './create-job-page.component.html',
  styleUrl: './create-job-page.component.scss'
})

export class CreateJobPageComponent implements OnInit {
  customers: any
  services: any
  materials: any
  contractors: any
  selectedCustomers: any = []
  selectedCustomersIsError = false
  selectedServices: any = []
  selectedServicesIsError = false
  selectedMaterials: any = []
  selectedMaterialsIsError = false
  selectedContractors: any = []
  selectedContractorsIsError = false
  materialInputFields: InputFieldDictionary[] = []
  status = 'created'
  description = ''
  address = ''
  city = ''
  state = ''
  zip = ''
  jobForm: FormGroup;
  states: any = []
  @ViewChild(InvoiceDatePickerComponent) datePicker!: InvoiceDatePickerComponent;

  readonly range = new FormGroup<DateRange>({
    issued: new FormControl<Date | null>(null),
    due: new FormControl<Date | null>(null),
  });

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

  setSelectedServices(services: number[]) {
    this.selectedServices = [...services]
    this.selectedServicesIsError = this.selectedServices.length === 0

    if (this.selectedServices.length !== 0) {
      this.selectedMaterials = []
      this.selectedMaterialsIsError = false
      this.loadMaterialsToTable("", 5, 0)
      this.selectedContractors = []
      this.selectedContractorsIsError = false
      this.loadContractorsToTable("", 5, 0)
    } else {
      this.selectedMaterials = []
      this.materials = { data: [], totalCount: 0 }
      this.selectedContractors = []
      this.contractors = { data: [], totalCount: 0 }
      this.selectedServicesIsError = true
    }
  }

  setSelectedMaterials(materials: number[]) {
    this.selectedMaterials = [...materials]
    this.selectedMaterialsIsError = this.selectedMaterials.length === 0

    if (!this.selectedMaterialsIsError) {
      const previousUnitsUsedFields = this.materialInputFields
      this.materialInputFields = []
      this.selectedMaterials.forEach((element: any) => {
        if (previousUnitsUsedFields.some((item) => item.id === element)) {
          const specificEntry = previousUnitsUsedFields.find((item) => item.id === element)
          this.materialInputFields.push({"id": element, "unitsUsed": specificEntry!["unitsUsed"], "pricePerUnit": specificEntry!["pricePerUnit"]})
        } else {
          this.materialInputFields.push({"id": element, "unitsUsed": 0, "pricePerUnit": 0.00})
        }

      });
    } else {
      this.materialInputFields = []
    }
  }

  setSelectedContractors(contractors: number[]) {
    this.selectedContractors = [...contractors]
    this.selectedContractorsIsError = this.selectedContractors.length === 0
  }

  setSelectedCustomers(cust: number[]) {
    this.selectedCustomers = [...cust]
    if (this.selectedCustomers.length !== 0) {
      this.selectedCustomersIsError = false
      this.selectedServices = []
      this.selectedServicesIsError = false
      this.loadServicesToTable("", 5, 0)
    }
    else {
      this.selectedServices = []
      this.services = { data: [], totalCount: 0 }
      this.selectedCustomersIsError = true
    }
  }

  setMaterialInput(inputField: InputFieldDictionary[]) {
    this.materialInputFields = inputField
  }

  setPricePerUnit(inputField: number) {
  }

  onSubmit() {
    const validDates = this.datePicker.validate()

    if (this.selectedCustomers.length === 0) {
      this.selectedCustomersIsError = true
      return;
    }
    if (this.selectedServices.length === 0) {
      const servicesTableVisible = this.selectedCustomers.length !== 0

      if (servicesTableVisible) {
        this.selectedServicesIsError = true
      }
      return;
    }

    if (!validDates) {
      return;
    }

    const servicesField: { id: any; } [] = []
    this.selectedServices.forEach((element: any) => {
      servicesField.push({ "id": element })
    })

    const contractorsField: { id: any; } [] = []
    this.selectedContractors.forEach((element: any) => {
      contractorsField.push({ "id": element })
    })

    if (this.jobForm.invalid) {
      this.jobForm.markAllAsTouched();
      return;
    } else {
    }

    const requestJson = {
      jobStatus: this.status,
      startDate: this.stringFormatter.dateFormatter(this.range.controls.issued.value),
      endDate: this.stringFormatter.dateFormatter(this.range.controls.due.value),
      description: this.jobForm.get('jobDescription')?.value,
      customerID: this.selectedCustomers[0],
      city: this.jobForm.get('requestorCity')?.value,
      state: this.jobForm.get('requestorStateSelect')?.value,
      zip: this.jobForm.get('requestorZip')?.value,
      address: this.jobForm.get('requestorAddress')?.value,
      contractors: contractorsField as [],
      services: servicesField as [],
      materials: this.materialInputFields as []
    }
    this.jobService.createJob(requestJson).subscribe(
      {
        next: () => {
          this.router.navigate(['/jobs']);
        },
        error: (error) => {
          this.errorHandler.handleError(error)
        }
      }
    )
    return;
  }
}
