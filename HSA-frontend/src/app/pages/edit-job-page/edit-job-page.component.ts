import { Component, SimpleChanges } from '@angular/core';
import { JobDataInterface } from '../../interfaces/api-responses/job.api.data.interface';
import { JobService } from '../../services/job.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ErrorHandlerService } from '../../services/error.handler.service';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { JobDisplayTableComponent } from '../../components/job-display-table/job-display-table.component';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { StringFormatter } from '../../utils/string-formatter';
import { MatSelectModule } from '@angular/material/select';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { AddSelectDialogComponentComponent } from '../../components/add-select-dialog-component/add-select-dialog-component.component';
import { MatDialog } from '@angular/material/dialog';
import { ServiceService } from '../../services/service.service';
import { MaterialService } from '../../services/material.service';
import { ContractorService } from '../../services/contractor.service';
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface'

interface State {
  name: string,
  code: string
}

@Component({
  selector: 'app-edit-job-page',
  providers: [
    provideNativeDateAdapter()
  ],
  imports: [
    LoadingFallbackComponent, 
    CommonModule, 
    MatButtonModule, 
    MatIconModule, 
    JobDisplayTableComponent, 
    MatCardModule,
    MatListModule,
    MatDividerModule,
    MatExpansionModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatSelectModule,
    MatDatepickerModule
  ],
  templateUrl: './edit-job-page.component.html',
  styleUrl: './edit-job-page.component.scss'
})
export class EditJobPageComponent {
  jobID!: number
  jobData: JobDataInterface | null = null;
  customers: any
  services: any
  materials: any
  contractors: any
  allServices: any = []
  allMaterials: any = []
  allContractors: any = []
  selectedServices: any = []
  selectedMaterials: any = []
  selectedContractors: any = []
  deletedCustomers: any = []
  deletedServices: any = []
  deletedMaterials: any = []
  deletedContractors: any = []
  materialInputFields: InputFieldDictionary[] = []
  status: 'created' | 'in-progress' | 'completed' = 'created'
  description: string = ''
  address: string = ''
  city: string = ''
  state: string = ''
  zip: string = ''
  jobForm: FormGroup;
  states: State[] = [];
  
  constructor (
    private jobService: JobService,
    private serviceService: ServiceService,
    private materialService: MaterialService,
    private contractorService: ContractorService,
    private activatedRoute:ActivatedRoute, 
    private router: Router, 
    private errorHandler: ErrorHandlerService,
    private jobFormBuilder: FormBuilder,
    private stringFormatter: StringFormatter, 
    private http: HttpClient,
    public dialog: MatDialog
  ) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.jobID = Number(params.get('id'));
    })

    this.jobForm = this.jobFormBuilder.group({
      customerName: ['', Validators.required],
      jobStatus: ['', Validators.required],
      startDate: [new Date(), Validators.required],
      endDate: [new Date(), Validators.required],
      jobDescription: ['', Validators.required],
      requestorAddress: [''],
      requestorCity: [''],
      requestorZip: [''],
      requestorStateSelect: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadStates()
    this.loadServicesToTable("", 5, 0)
    this.loadMaterialsToTable("", 5, 0)
    this.loadContractorsToTable("", 5, 0)

    this.jobService.getSpecificJobData(this.jobID).subscribe(
      {next: (response) => {
        this.jobData = response

        this.jobForm.setValue({
          customerName: this.jobData?.data.customerName,
          jobStatus: this.jobData?.data.jobStatus,
          startDate: this.jobData?.data.startDate,
          endDate: this.jobData?.data.endDate,
          jobDescription: this.jobData?.data.description,
          requestorAddress: this.jobData?.data.requestorAddress,
          requestorCity: this.jobData?.data.requestorCity,
          requestorZip: this.jobData?.data.requestorZip,
          requestorStateSelect: this.jobData?.data.requestorState,
        })

        this.services = this.jobData.services
        this.materials = this.jobData.materials
        this.contractors = this.jobData.contractors
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }}
    )
  }

  loadStates() {
    this.http.get<State[]>('states.json').subscribe(
      (data: State[]) => {
        this.states = data;
      }
    )
  }

  loadServicesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.serviceService.getService({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.services = response
        this.allServices = response
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
        this.allMaterials = response
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
        this.allContractors = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  setSelectedServices(services: number[]) {
    this.selectedServices = [...services]
  }

  setSelectedMaterials(materials: number[]) {
    this.selectedMaterials = [...materials]
    let previousUnitsUsedFields = this.materialInputFields
    this.selectedMaterials.forEach((element: any) => {
      if (previousUnitsUsedFields.some((item) => item.id === element)) {
        let specificEntry = previousUnitsUsedFields.find((item) => item.id === element)
        this.materialInputFields.push({"id": element, "unitsUsed": specificEntry!["unitsUsed"], "pricePerUnit": specificEntry!["pricePerUnit"]})
      } else {
        this.materialInputFields.push({"id": element, "unitsUsed": 0, "pricePerUnit": 0.00})
      }
      
    });
  }

  setSelectedContractors(contractors: number[]) {
    this.selectedContractors = [...contractors]
  }

  setMaterialInput(inputField: InputFieldDictionary[]) {
    this.materialInputFields = inputField
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }

  openAddServiceDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'service',
      dialogData: this.allServices,
      loadData: this.loadServicesToTable.bind(this),
      setSelectedItems: this.setSelectedServices,
      searchHint: 'Search by material name',
      headers: ['Service Name', 'Service Description'],
      materialInputFields: this.materialInputFields,
      setMaterialInputFields: this.setMaterialInput
    }

    const dialogRef = this.dialog.open(AddSelectDialogComponentComponent, {
      width: 'auto', 
      maxWidth: '90vw', 
      height: 'auto', 
      maxHeight: '90vh', 
      data: dialogData
    });

    setTimeout(() => {
      document.getElementById('modal')?.removeAttribute('aria-hidden');
    }, 10);
  }

  openAddMaterialDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'material',
      dialogData: this.allMaterials,
      loadData: this.loadMaterialsToTable.bind(this),
      setSelectedItems: this.setSelectedMaterials,
      searchHint: 'Search by material name or description',
      headers: ['Checkbox', 'Material Name', 'Material Description'],
      materialInputFields: this.materialInputFields,
      setMaterialInputFields: this.setMaterialInput
    }

    const dialogRef = this.dialog.open(AddSelectDialogComponentComponent, {
      width: 'auto', 
      maxWidth: '90vw', 
      height: 'auto', 
      maxHeight: '90vh', 
      data: dialogData
    });

    setTimeout(() => {
      document.getElementById('modal')?.removeAttribute('aria-hidden');
    }, 10);
  }

  openAddContractorDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'contractor',
      dialogData: this.allContractors,
      loadData: this.loadContractorsToTable.bind(this),
      setSelectedItems: this.setSelectedContractors,
      searchHint: 'Search by contractor name or description',
      headers: ['Checkbox', 'Contractor Name', 'Phone Number', 'Email'],
      materialInputFields: this.materialInputFields,
      setMaterialInputFields: this.setMaterialInput
    }

    const dialogRef = this.dialog.open(AddSelectDialogComponentComponent, {
      width: 'auto', 
      maxWidth: '90vw', 
      height: 'auto', 
      maxHeight: '90vh', 
      data: dialogData
    });

    setTimeout(() => {
      document.getElementById('modal')?.removeAttribute('aria-hidden');
    }, 10);
  }

  onDelete(typeToDelete: string, data: any, joinRelationID: any): any {
    switch (typeToDelete) {
      case 'service': {
        let popOutID = data["Service ID"];
        this.deletedServices.push(joinRelationID);
        this.services.services = this.services.services.filter((item: { serviceID: any; }) => item.serviceID !== popOutID);
        return this.services;
      }
      case 'material': {
        let popOutID = data["Material ID"];
        this.deletedMaterials.push(joinRelationID);
        this.materials.materials = this.materials.materials.filter((item: { materialID: any; }) => item.materialID !== popOutID);
        return this.materials;
      }
      case 'contractor': {
        let popOutID = data["Contractor ID"];
        this.deletedContractors.push(joinRelationID);
        this.contractors.contractors = this.contractors.contractors.filter((item: { contractorID: any; }) => item.contractorID !== popOutID);
        return this.contractors;
      }  
      
    }
  }

  onSubmit() {}
}
