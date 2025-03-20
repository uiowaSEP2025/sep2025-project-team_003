import { Component, OnInit, ViewChild } from '@angular/core';
import { InvoiceDatePickerComponent } from '../../components/invoice-date-picker/invoice-date-picker.component';
import { CustomerService } from '../../services/customer.service';
import { Router } from '@angular/router';
import { StringFormatter } from '../../utils/string-formatter';
import { ErrorHandlerService } from '../../services/error.handler.service';
import { FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatError, MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { LoadingFallbackComponent } from "../../components/loading-fallback/loading-fallback.component";
import { ServiceService } from '../../services/service.service';
import { MaterialService } from '../../services/material.service';
import { ContractorService } from '../../services/contractor.service';
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { DateRange } from '../edit-invoice-page/edit-invoice-page.component';
import { JobService } from '../../services/job.service';
import { HttpClient } from '@angular/common/http';

interface State {
  name: string,
  code: string
}

@Component({
  selector: 'app-create-job-page',
  imports: [
    TableComponentComponent,
    CommonModule,
    MatButtonModule,
    MatError,
    FormsModule,
    MatFormFieldModule,
    InvoiceDatePickerComponent,
    MatSelectModule,
    MatInputModule,
    LoadingFallbackComponent,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule
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
  selectedCustomersIsError: boolean = false
  selectedServices: any = []
  selectedServicesIsError: boolean = false
  selectedMaterials: any = []
  selectedMaterialsIsError: boolean = false
  selectedContractors: any = []
  selectedContractorsIsError: boolean = false
  materialInputFields: InputFieldDictionary[] = []
  materialInputFieldsIsError: boolean = false
  status: string = 'created'
  description: string = ''
  address: string = ''
  city: string = ''
  state: string = ''
  zip: string = ''
  jobForm: FormGroup;
  states: State[] = [];
  @ViewChild(InvoiceDatePickerComponent) datePicker!: InvoiceDatePickerComponent;

  readonly range: FormGroup<DateRange> = new FormGroup({
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
    private http: HttpClient
  ) { 
    this.jobForm = this.jobFormBuilder.group({
      requestorAddress: [''],
      requestorCity: [''],
      requestorZip: [''],
      requestorStateSelect: ['', Validators.required],
      jobDescription: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadCustomersToTable("", 5, 0);
    this.loadStates()
  }

  loadStates() {
    this.http.get<State[]>('states.json').subscribe(
      (data: State[]) => {
        this.states = data;
      }
    )
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
        console.log(this.contractors)
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  setSelectedServices(services: number[]) {
    this.selectedServices = [...services]
    this.selectedServicesIsError = this.selectedServices.length === 0 ? true : false

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
    this.selectedMaterialsIsError = this.selectedMaterials.length === 0 ? true : false

    if (this.selectedMaterialsIsError === false) {
      let previousUnitsUsedFields = this.materialInputFields
      this.materialInputFields = []
      this.selectedMaterials.forEach((element: any) => {
        if (previousUnitsUsedFields.some((item) => item.id === element)) {
          let specificEntry = previousUnitsUsedFields.find((item) => item.id === element)
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
    this.selectedContractorsIsError = this.selectedContractors.length === 0 ? true : false
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
    console.log(this.materialInputFields)
  }

  setPricePerUnit(inputField: number) {
  }

  onSubmit() {
    let validDates: any
    validDates = this.datePicker.validate()

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

    let servicesField: { id: any; } [] = []
    this.selectedServices.forEach((element: any) => {
      servicesField.push({ "id": element })
    })

    let contractorsField: { id: any; } [] = []
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
    console.log(requestJson)
    this.jobService.createJob(requestJson).subscribe(
      {
        next: (response) => {
          console.log(response)
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
