import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { ServiceService } from '../../services/service.service';
import { MaterialService } from '../../services/material.service';
import { CustomerService } from '../../services/customer.service';
import { JobService } from '../../services/job.service';
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { MatError, MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButton } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog } from '@angular/material/dialog';
import { AddConfirmDialogComponentComponent } from '../../components/add-confirm-dialog-component/add-confirm-dialog-component.component';
import { ContractorService } from '../../services/contractor.service';
import { OrganizationService } from '../../services/organization.service';
import { Router } from '@angular/router';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { JobDisplayTableComponent } from '../../components/job-display-table/job-display-table.component';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSelectModule } from '@angular/material/select';
import { JobTemplateService } from '../../services/jobTemplate.service';
import { StringFormatter } from '../../utils/string-formatter';
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface';
import { AddSelectDialogComponentComponent } from '../../components/add-select-dialog-component/add-select-dialog-component.component';
import { StateList } from '../../utils/states-list';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-onboarding-page',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatStepperModule,
    MatCardModule,
    FormsModule,
    ReactiveFormsModule,
    MatButton,
    MatDatepickerModule,
    JobDisplayTableComponent,
    MatExpansionModule,
    MatSelectModule,
    MatError
  ],
  providers: [
    provideNativeDateAdapter()
  ],
  templateUrl: './onboarding-page.component.html',
  styleUrl: './onboarding-page.component.scss'
})
export class OnboardingPageComponent implements OnInit {
  serviceForm: FormGroup;
  materialForm: FormGroup;
  customerForm: FormGroup;
  contractorForm: FormGroup;
  jobGeneralForm: FormGroup;
  firstService: any;
  firstCustomer: any;
  firstMaterial: any;
  firstContractor: any;
  organization: any;

  jobID!: number | null
  customerID: number = 0
  customers: any
  services: any
  materials: any
  contractors: any
  selectedCustomer: number = 0
  selectedServices: any = []
  selectedMaterials: any = []
  selectedContractors: any = []
  materialInputFields: InputFieldDictionary[] = []
  deletedCustomers: any = []
  deletedJobServices: any = []
  deletedJobMaterials: any = []
  deletedJobContractors: any = []
  status: string = 'created'
  states: any = []
  isServicePrefilled: boolean = false
  isMaterialPrefilled: boolean = false
  isCustomerPrefilled: boolean = false
  isContractorPrefilled: boolean = false
  isJobPrefilled: boolean = false
  @ViewChild('stepper') stepper!: MatStepper;

  constructor(
    private router: Router, 
    private serviceFormBuilder: FormBuilder,
    private materialFormBuilder: FormBuilder,
    private customerFormBuilder: FormBuilder,
    private contractorFormBuilder: FormBuilder,
    private organizationService: OrganizationService,
    private serviceService: ServiceService,
    private materialService: MaterialService,
    private customerService: CustomerService,
    private contractorService: ContractorService,
    private jobService: JobService,
    private stringFormatter: StringFormatter, 
    private jobFormBuilder: FormBuilder,
    public dialog: MatDialog,
    private snackBar: MatSnackBar,
  ) {
    this.serviceForm = this.serviceFormBuilder.group({
      serviceName: ['', Validators.required],
      serviceDescription: ['', Validators.required]
    })

    this.materialForm = this.materialFormBuilder.group({
      materialName: ['']
    })

    this.customerForm = this.customerFormBuilder.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', Validators.required],
      note: ['']
    })

    this.contractorForm = this.contractorFormBuilder.group({
      firstName: [''],
      lastName: [''],
      email: ['', Validators.email],
      phone: [''],
    })

    this.states = StateList.getStates()
    
    this.jobGeneralForm = this.jobFormBuilder.group({
      customerName: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: ['', Validators.required],
      requestorAddress: ['', Validators.required],
      requestorCity: ['', Validators.required],
      requestorZip: ['', Validators.required],
      requestorStateSelect: ['', Validators.required],
      jobDescription: ['', Validators.required]
    }, { validators: this.dateValidator });

    this.services = { "services": [] };
    this.materials = { "materials": [] };
    this.contractors = { "contractors": [] };
  }

  ngOnInit(): void {
    this.organizationService.getOrganization().subscribe({
      next: (response) => {
        this.organization = response

        if (this.organization["is_onboarding"] === false) {
          this.navigateToPage('home')
        }
      },
      error: (error) => {
      }
    })
  }

  onSubmitServiceCreation() {
    if (this.serviceForm.invalid) {
      this.serviceForm.markAllAsTouched()
    } else {
      const serviceCreateRequest = {
        service_name: this.serviceForm.get("serviceName")?.value,
        service_description: this.serviceForm.get("serviceDescription")?.value
      }

      this.serviceService.createService(serviceCreateRequest).subscribe({
        next: (response) => {
          this.firstService = response
        },
        error: (error) => {
        }
      })

      this.stepper.selected!.completed = true;
      this.stepper.next();
    }
  }

  onSubmitMaterialCreation() {
    if (this.materialForm.get("materialName")?.value !== "") {
      const materialCreateRequest = {
        material_name: this.materialForm.get("materialName")?.value,
      }

      this.materialService.createMaterial(materialCreateRequest).subscribe({
        next: (response) => {
          this.firstMaterial = response
        },
        error: (error) => {
        }
      })
    }

    this.stepper.selected!.completed = true;
    this.stepper.next();
  }

  onSubmitCustomerCreation() {
    if (this.customerForm.invalid) {
      this.customerForm.markAllAsTouched()
    } else {
      const customerCreateRequest = {
        firstn: this.customerForm.get('firstName')?.value,
        lastn: this.customerForm.get('lastName')?.value,
        email: this.customerForm.get('email')?.value,
        phoneno: this.customerForm.get('phone')?.value,
        notes: this.customerForm.get('note')?.value,
      }

      this.customerService.createCustomer(customerCreateRequest).subscribe({
        next: (response) => {
          this.firstCustomer = response
        },
        error: (error) => {
        }
      });

      this.stepper.selected!.completed = true;
      this.stepper.next();
    }
  }

  onSubmitContractorCreation() {
    if (this.contractorForm.get('firstName')?.value !== "" 
    && this.contractorForm.get('lastName')?.value !== ""
    && this.contractorForm.get('email')?.value !== ""
    && this.contractorForm.get('phone')?.value !== ""
  ) {
      const contractorCreateRequest = {
        firstName: this.contractorForm.get('firstName')?.value,
        lastName: this.contractorForm.get('lastName')?.value,
        email: this.contractorForm.get('email')?.value,
        phone: this.contractorForm.get('phone')?.value,
      }

      this.contractorService.createContractor(contractorCreateRequest).subscribe({
        next: (response) => {
          this.firstContractor = response
        },
        error: (error) => {
        }
      });
    }

    this.stepper.selected!.completed = true;
    this.stepper.next();
  }

  
  onSubmitJobGeneral() {
    if (this.jobGeneralForm.invalid) {
      this.jobGeneralForm.markAllAsTouched();
      this.stepper.selected!.completed = false;
    } else {
      this.stepper.selected!.completed = true;
      this.stepper.next();
    }
  }

  openPrefillDialog(type: string) {
    const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
      width: '300px',
      data: "prefill data? (All prefill data will not be saved)"
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        switch (type) {
          case "service":
            this.serviceForm.setValue({
              serviceName: "Example Service",
              serviceDescription: "Example Service Description"
            });
            this.isServicePrefilled = true;
            break;
          case "customer":
            this.customerForm.setValue({
              firstName: "First",
              lastName: "Last",
              email: "first.last@example.com",
              phone: "000-000-0000",
              note: "Example Note"
            });
            this.isCustomerPrefilled = true;
            break;
          case "material":
            this.materialForm.setValue({
              materialName: "Example Material"
            });
            this.isMaterialPrefilled = true;
            break;
          case "contractor":
            this.contractorForm.setValue({
              firstName: "FirstCon",
              lastName: "LastCon",
              email: "firstCon.lastCon@example.com",
              phone: "000-000-0000",
            });
            this.isContractorPrefilled = true
            break;
          case "job":
            this.jobGeneralForm.setValue({
              customerName: this.firstCustomer.data["first_name"] + " " + this.firstCustomer.data["last_name"],
              startDate: new Date("01/01/1999"),
              endDate: new Date("01/02/1999"),
              requestorAddress: "9999 Example Address",
              requestorCity: "Example City",
              requestorZip: "99999",
              requestorStateSelect: this.organization["org_requestor_state"],
              jobDescription: "Example Job Description"
            });

            this.customerID = this.firstCustomer.data["id"];
            this.selectedCustomer = this.firstCustomer.data["id"]
            this.isJobPrefilled = true;
            break;
        }
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
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
  
  openAddCustomerDialog() {
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
        let customerEntry = result.itemsInfo[0]
        this.jobGeneralForm.controls['customerName'].setValue(customerEntry.first_name + " " + customerEntry.last_name)
        this.customerID = customerEntry.id;
        this.selectedCustomer = customerEntry.id
      }
    })
  }

  openAddServiceDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'service',
      dialogData: this.services,
      searchHint: 'Search by material name',
      headers: ['Service Name', 'Service Description'],
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
        result.itemsInfo.forEach((element: { [x: string]: any; }) => {
          let info: any = {};
          info['id'] = 0;
          info['serviceID'] = element['id'];
          info['serviceName'] = element['service_name'];
          info['serviceDescription'] = element['service_description'];
          this.services = { services: [...this.services.services, info] };
        });
      
        this.selectedServices = result.selectedItems;
      }
    });
  }

  openAddMaterialDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'material',
      dialogData: this.materials,
      searchHint: 'Search by material name or description',
      headers: ['Checkbox', 'Material Name', 'Material Description'],
      materialInputFields: this.materialInputFields,
    }

    const dialogRef = this.dialog.open(AddSelectDialogComponentComponent, {
      width: 'auto', 
      maxWidth: '90vw', 
      height: 'auto', 
      maxHeight: '90vh', 
      data: dialogData
    });

    dialogRef.afterClosed().subscribe((result:any) => {
      if (result.length !== 0) {
        result.itemsInfo.forEach((element: any) => {
          this.materials = { materials: [...this.materials.materials, element] };
        });

        this.selectedMaterials = result.selectedItems;
      }
    });
  }

  openAddContractorDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'contractor',
      dialogData: this.contractors,
      searchHint: 'Search by contractor name or description',
      headers: ['Checkbox', 'Contractor Name', 'Phone Number', 'Email'],
      materialInputFields: this.materialInputFields,
    }

    const dialogRef = this.dialog.open(AddSelectDialogComponentComponent, {
      width: 'auto', 
      maxWidth: '90vw', 
      height: 'auto', 
      maxHeight: '90vh', 
      data: dialogData
    });

    dialogRef.afterClosed().subscribe((result:any) => {
      if (result.length !== 0) {
        result.itemsInfo.forEach((element: { [x: string]: any; }) => {
          let info: any = {};
          info['id'] = 0;
          info['contractorID'] = element['id'];
          info['contractorName'] = element['first_name'] + " " + element['last_name'];
          info['contractorPhoneNo'] = element['phone'];
          info['contractorEmail'] = element['email'];
          this.contractors = { contractors: [...this.contractors.contractors, info] };
        });

        this.selectedContractors = result.selectedItems;
      }
    });
  }

  onDelete(typeToDelete: string, data: any, joinRelationID: any, itemID: any): any {
    switch (typeToDelete) {
      case 'service': {
        let popOutID = data["Service ID"];

        if (joinRelationID !== 0) {
          this.deletedJobServices.push(joinRelationID);
        } else {
          this.selectedServices = this.selectedServices.filter((item: any) => item !== itemID)
        }

        this.services.services = this.services.services.filter((item: { serviceID: any; }) => item.serviceID !== popOutID);
        return this.services;
      }
      case 'material': {
        let popOutID = data["Material ID"];

        if (joinRelationID !== 0) {
          this.deletedJobMaterials.push(joinRelationID);
        } else {
          this.selectedMaterials = this.selectedMaterials.filter((item: any) => item.id !== itemID)
        }

        this.materials.materials = this.materials.materials.filter((item: { materialID: any; }) => item.materialID !== popOutID);
        return this.materials;
      }
      case 'contractor': {
        let popOutID = data["Contractor ID"];
        
        if (joinRelationID !== 0) {
          this.deletedJobContractors.push(joinRelationID);
        } else {
          this.selectedContractors = this.selectedContractors.filter((item: any) => item !== itemID)
        }

        this.contractors.contractors = this.contractors.contractors.filter((item: { contractorID: any; }) => item.contractorID !== popOutID);
        return this.contractors;
      }  
    };
    
  }

  onCreateConfirmDialog(type: string) {
    if (type === 'job') {
      const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
        data: "job creation"
      });
  
      dialogRef.afterClosed().subscribe((result:any) => {
        if (result) {
          this.onSubmit();
        }
      });
    }  
  }

  onSubmit() {
    if (this.jobGeneralForm.invalid) {
      this.jobGeneralForm.markAllAsTouched();
      this.snackBar.open('Invalid fields, please revise the form and resubmit', '', {
        duration: 3000
      });
    }

    if (this.isJobPrefilled) {
      this.deleteAllPrefilledEntries();
      this.updateOnboardingField();
      this.navigateToPage('home');
      return;
    } else {
      let servicesField: { id: any; } [] = []
      this.services.services.forEach((element: any) => {
        servicesField.push({ "id": element["serviceID"] })
      })
  
      let materialsField: { id: any, unitsUsed: any, pricePerUnit: any} [] = []
      this.materials.materials.forEach((element: any) => {
        materialsField.push({ 
          "id": element["materialID"],
          "unitsUsed": element["unitsUsed"],
          "pricePerUnit": element["pricePerUnit"] 
        });
      });
  
      let contractorsField: { id: any; } [] = []
      this.contractors.contractors.forEach((element: any) => {
        contractorsField.push({ "id": element["contractorID"] })
      });
      
      const requestJson = {
        jobStatus: this.status,
        startDate: this.stringFormatter.dateFormatter(this.jobGeneralForm.get('startDate')?.value),
        endDate: this.stringFormatter.dateFormatter(this.jobGeneralForm.get('endDate')?.value),
        description: this.jobGeneralForm.get('jobDescription')?.value,
        customerID: this.selectedCustomer,
        city: this.jobGeneralForm.get('requestorCity')?.value,
        state: this.jobGeneralForm.get('requestorStateSelect')?.value,
        zip: this.jobGeneralForm.get('requestorZip')?.value,
        address: this.jobGeneralForm.get('requestorAddress')?.value,
        contractors: contractorsField as [],
        services: servicesField as [],
        materials: materialsField as []
      }
  
      this.jobService.createJob(requestJson).subscribe(
        {
          next: (response) => {
            this.snackBar.open('Job create successfully', '', {
              duration: 3000
            });
  
            this.deleteAllPrefilledEntries();
            this.updateOnboardingField();
            this.navigateToPage('home');
          },
          error: (error) => {
          }
        }
      )
      return;
    }
  }

  onCancelOnboaring() {
    const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
      width: '500px',
      data: "cancel of the onboaring process? (All steps will be lost)"
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deleteAllPrefilledEntries();
        this.navigateToPage('home');
      }
    });
  }

  deleteAllPrefilledEntries() {
    let serviveID = this.firstService.data["id"]
    let materialID = this.materialForm.get("materialName")?.value !== "" ? this.firstMaterial.data["id"] : 0
    let customerID = this.firstCustomer.data["id"]
    let contractorID = this.contractorForm.get("firstName")?.value !== "" ? this.firstContractor.data["id"] : 0

    if (this.isServicePrefilled) {
      this.serviceService.deleteService({ id: serviveID, service_name: this.firstService["service_name"] }).subscribe({
        next: (response) => {

        },
        error: (error) => {
        }
      })
    }

    if (this.isMaterialPrefilled) {
      this.materialService.deleteMaterial({ id: materialID, material_name: this.firstMaterial["material_name"] }).subscribe({
        next: (response) => {

        },
        error: (error) => {
        }
      })
    }

    if (this.isCustomerPrefilled) {
      this.customerService.deleteCustomer({ id: customerID, firstn: this.firstCustomer["first_name"], lastn: this.firstCustomer["last_name"] }).subscribe({
        next: (response) => {

        },
        error: (error) => {
        }
      })
    }

    if (this.isContractorPrefilled) {
      this.contractorService.deleteContractor({ id: contractorID }).subscribe({
        next: (response) => {

        },
        error: (error) => {
        }
      })
    }
  }

  updateOnboardingField() {
    const organizationUpdateData = {
      name: this.organization["org_name"],
      email: this.organization["org_email"],
      city: this.organization["org_city"],
      phone: this.organization["org_phone"],
      requestorState: this.organization["org_requestor_state"],
      requestorZip: this.organization["org_requestor_zip"],
      requestorAddress: this.organization["org_requestor_address"],
      ownerFn: this.organization["org_owner_first_name"],
      ownerLn: this.organization["org_owner_last_name"],
      isOnboarding: false
    }

    this.organizationService.editOrganization(organizationUpdateData).subscribe({
      next: (response) => {
        this.snackBar.open('Onboarding completed!', '', {
          duration: 3000
        });
      },
      error: (error) => {
      }
    });
  }
}
