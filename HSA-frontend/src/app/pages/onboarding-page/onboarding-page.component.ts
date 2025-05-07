import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { MatError, MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButton } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog } from '@angular/material/dialog';
import { AddConfirmDialogComponentComponent } from '../../components/add-confirm-dialog-component/add-confirm-dialog-component.component';
import { OrganizationService } from '../../services/organization.service';
import { Router } from '@angular/router';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { JobDisplayTableComponent } from '../../components/job-display-table/job-display-table.component';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSelectModule } from '@angular/material/select';
import { StringFormatter } from '../../utils/string-formatter';
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface';
import { StateList } from '../../utils/states-list';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OnboardingSelectDialogComponentComponent } from '../../components/onboarding-select-dialog-component/onboarding-select-dialog-component.component';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { currencyValidator } from '../../utils/currency-validator';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';

@Component({
  selector: 'app-onboarding-page',
  imports: [
    MatTooltipModule,
    MatFormFieldModule,
    MatIconModule,
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
    MatError,
    PageTemplateComponent
  ],
  providers: [
    provideNativeDateAdapter()
  ],
  templateUrl: './onboarding-page.component.html',
  styleUrl: './onboarding-page.component.scss'
})
export class OnboardingPageComponent implements OnInit {
  buttonForm: FormGroup;
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
  isExamplePrefilled: boolean = false
  isLockedServiceStep: boolean = false
  isLockedCustomerStep: boolean = false
  isLockedMaterialStep: boolean = false
  isLockedContractorStep: boolean = false
  phonePattern: RegExp = /^\d{3}-\d{3}-\d{4}$/;
  @ViewChild('stepper') stepper!: MatStepper;

  constructor(
    private router: Router,
    private buttonFormBuilder: FormBuilder,
    private serviceFormBuilder: FormBuilder,
    private materialFormBuilder: FormBuilder,
    private customerFormBuilder: FormBuilder,
    private contractorFormBuilder: FormBuilder,
    private organizationService: OrganizationService,
    private stringFormatter: StringFormatter,
    private jobFormBuilder: FormBuilder,
    public dialog: MatDialog,
    private snackBar: MatSnackBar,
  ) {
    this.buttonForm = this.buttonFormBuilder.group({
      exampleConfirmation: ['', Validators.required]
    })

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
      requestorStateSelect: [, Validators.required],
      jobDescription: ['', Validators.required],
      flatfee: ['0.00', [Validators.required, currencyValidator()]],
      hourlyRate: ['0.00', [Validators.required, currencyValidator()]],
      minutesWorked: ['0', [Validators.required, Validators.min(0)]],
    }, { validators: this.dateValidator });

    this.services = { "services": [] };
    this.materials = { "materials": [] };
    this.contractors = { "contractors": [] };
  }

  ngOnInit(): void {
    this.organizationService.getOrganization().subscribe({
      next: (response) => {
        this.organization = response
        this.jobGeneralForm.patchValue({
          requestorStateSelect: this.organization["org_requestor_state"]
        })

        if (this.organization["is_onboarding"] === false) {
          this.navigateToPage('home')
        }
      },
      error: (error) => {
      }
    })
  }

  onYesNoConfirm(isYes: string) {
    if (isYes === "yes") {
      const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
        width: "400px",
        data: "with prefilled data (All steps will not be saved)"
      });

      dialogRef.afterClosed().subscribe((result: any) => {
        if (result) {
          this.buttonForm.patchValue({
            exampleConfirmation: isYes
          })

          this.buttonForm.markAsTouched();
          this.stepper.next()

          this.isExamplePrefilled = true
          this.prefillInfo()
        }
      });
    } else {
      this.buttonForm.patchValue({
        exampleConfirmation: isYes
      })

      this.isExamplePrefilled = false
      this.buttonForm.markAsTouched();
      this.stepper.next()
    }
  }

  onSubmitServiceCreation() {
    if (this.serviceForm.invalid) {
      this.serviceForm.markAllAsTouched()
    } else {
      const serviceCreateResponse = {
        id: 1,
        service_name: this.serviceForm.get("serviceName")?.value,
        service_description: this.serviceForm.get("serviceDescription")?.value
      }

      this.firstService = serviceCreateResponse

      this.stepper.selected!.completed = true;
      this.stepper.next();
    }
  }

  onSubmitMaterialCreation() {
    if (this.materialForm.get("materialName")?.value !== "") {
      const materialCreateResponse = {
        id: 1,
        material_name: this.materialForm.get("materialName")?.value,
      }

      this.firstMaterial = materialCreateResponse
    } else {
      this.materials.materials = []
    }

    this.stepper.selected!.completed = true;
    this.stepper.next();
  }

  onSubmitCustomerCreation() {
    if (this.customerForm.invalid) {
      this.customerForm.markAllAsTouched()
    } else {
      const customerCreateResponse = {
        id: 1,
        first_name: this.customerForm.get('firstName')?.value,
        last_name: this.customerForm.get('lastName')?.value,
        email: this.customerForm.get('email')?.value,
        phone_no: this.customerForm.get('phone')?.value,
      }

      this.firstCustomer = customerCreateResponse
      this.customerID = this.firstCustomer["id"];
      this.selectedCustomer = this.firstCustomer["id"]
      this.isLockedCustomerStep = true
      this.stepper.selected!.completed = true;
      this.stepper.next();
    }
  }

  onSubmitContractorCreation() {
    if (this.contractorForm.get('firstName')?.value !== ""
      && this.contractorForm.get('lastName')?.value !== ""
      && this.contractorForm.get('email')?.value !== ""
      && this.contractorForm.get('phone')?.value !== ""
      && this.phonePattern.test(this.contractorForm.get('phone')?.value || '')
    ) {
      const contractorCreateResponse = {
        id: 1,
        first_name: this.contractorForm.get('firstName')?.value,
        last_name: this.contractorForm.get('lastName')?.value,
        email: this.contractorForm.get('email')?.value,
        phone: this.contractorForm.get('phone')?.value,
      }

      this.firstContractor = contractorCreateResponse
      this.stepper.selected!.completed = true;
      this.stepper.next();
    } else {
      this.firstContractor = null
      this.contractors.contractors = []


      if (this.contractorForm.get('firstName')?.value === ""
        && this.contractorForm.get('lastName')?.value === ""
        && this.contractorForm.get('email')?.value === ""
        && (this.contractorForm.get('phone')?.value === ""
          || this.phonePattern.test(this.contractorForm.get('phone')?.value || ''))) {
        this.stepper.selected!.completed = true;
        this.stepper.next();
      } else {
        this.snackBar.open('Cannot proceed with any invalid field, please clear or fill up all fields!', '', {
          duration: 3000
        });
        this.contractorForm.markAllAsTouched();
        this.stepper.selected!.completed = false;
      }
    }
  }


  onSubmitJobGeneral() {
    if (this.jobGeneralForm.invalid) {
      this.jobGeneralForm.markAllAsTouched();
      this.snackBar.open('Invalid fields, please revise the form and resubmit', '', {
        duration: 3000
      });

      this.stepper.selected!.completed = false;
    } else {
      this.stepper.selected!.completed = true;
      this.stepper.next();
    }
  }

  prefillInfo() {
    this.serviceForm.setValue({
      serviceName: "Example Service",
      serviceDescription: "Example Service Description"
    });

    this.customerForm.setValue({
      firstName: "First",
      lastName: "Last",
      email: "first.last@example.com",
      phone: "000-000-0000",
      note: "Example Note"
    });

    this.materialForm.setValue({
      materialName: "Example Material"
    });

    this.contractorForm.setValue({
      firstName: "FirstCon",
      lastName: "LastCon",
      email: "firstCon.lastCon@example.com",
      phone: "000-000-0000",
    });

    this.jobGeneralForm.setValue({
      customerName: "First Last",
      startDate: new Date("01/01/1999"),
      endDate: new Date("01/02/1999"),
      requestorAddress: "9999 Example Address",
      requestorCity: "Example City",
      requestorZip: "99999",
      requestorStateSelect: this.organization["org_requestor_state"],
      jobDescription: "Example Job Description"
    });
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
    this.customers = {
      customers: [this.firstCustomer]
    }

    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'customer',
      dialogData: this.customers,
      searchHint: 'Search by customer name',
      headers: ['First Name', 'Last Name', 'Email', 'Phone No'],
      materialInputFields: this.materialInputFields,
    };

    const dialogRef = this.dialog.open(OnboardingSelectDialogComponentComponent, {
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
      dialogData: {
        services: [this.firstService]
      },
      searchHint: 'Search by material name',
      headers: ['Service Name', 'Service Description'],
      materialInputFields: this.materialInputFields,
    };

    const dialogRef = this.dialog.open(OnboardingSelectDialogComponentComponent, {
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
          this.services = { services: [info] };
        });

        this.isLockedServiceStep = true;
        this.selectedServices = result.selectedItems;
      }
    });
  }

  openAddMaterialDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'material',
      dialogData: this.firstMaterial ? { materials: [this.firstMaterial] } : { materials: [] },
      searchHint: 'Search by material name or description',
      headers: ['Checkbox', 'Material Name', 'Material Description'],
      materialInputFields: this.materialInputFields,
    }

    const dialogRef = this.dialog.open(OnboardingSelectDialogComponentComponent, {
      width: 'auto',
      maxWidth: '90vw',
      height: 'auto',
      maxHeight: '90vh',
      data: dialogData
    });

    dialogRef.afterClosed().subscribe((result: any) => {
      if (result.length !== 0) {
        result.itemsInfo.forEach((element: any) => {
          this.materials = { materials: [element] };
        });

        this.isLockedMaterialStep = true;
        this.selectedMaterials = result.selectedItems;
      } else {
        this.materials.materials = []
      }
    });
  }

  openAddContractorDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'contractor',
      dialogData: this.firstContractor ? {
        contractors: [this.firstContractor]
      } : { contractors: [] },
      searchHint: 'Search by contractor name or description',
      headers: ['Checkbox', 'Contractor Name', 'Phone Number', 'Email'],
      materialInputFields: this.materialInputFields,
    }

    const dialogRef = this.dialog.open(OnboardingSelectDialogComponentComponent, {
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
          info['contractorID'] = element['id'];
          info['contractorName'] = element['first_name'] + " " + element['last_name'];
          info['contractorPhoneNo'] = element['phone'];
          info['contractorEmail'] = element['email'];
          this.contractors = { contractors: [info] };
        });

        this.isLockedContractorStep = true;
        this.selectedContractors = result.selectedItems;
      } else {
        this.contractors.contractors = []
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
        this.isLockedServiceStep = this.services.services.length !== 0
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
        this.isLockedMaterialStep = this.materials.materials.length !== 0
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
        this.isLockedContractorStep = this.contractors.contractors.length !== 0
        return this.contractors;
      }
    };

  }

  onCreateConfirmDialog(type: string) {
    if (type === 'job') {
      const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
        width: "400px",
        data: `job creation. ${this.isExamplePrefilled ? "(Example data will not be saved)" : ""}`
      });

      dialogRef.afterClosed().subscribe((result: any) => {
        if (result) {
          this.onSubmit();
        }
      });
    }
  }

  onSubmit() {
    const customerCreateRequest = !this.isExamplePrefilled ? {
      firstn: this.customerForm.get('firstName')?.value,
      lastn: this.customerForm.get('lastName')?.value,
      email: this.customerForm.get('email')?.value,
      phoneno: this.customerForm.get('phone')?.value,
      notes: this.customerForm.get('note')?.value,
    } : false

    const serviceCreateRequest = !this.isExamplePrefilled ? {
      service_name: this.serviceForm.get('serviceName')?.value,
      service_description: this.serviceForm.get('serviceDescription')?.value
    } : false

    const materialCreateRequest = !this.isExamplePrefilled ? this.materials.materials.length !== 0 ? {
      material_name: this.materialForm.get('materialName')?.value
    } : [] : false

    const contractorCreateRequest = !this.isExamplePrefilled ? this.contractors.contractors.length !== 0 ? {
      firstName: this.contractorForm.get('firstName')?.value,
      lastName: this.contractorForm.get('lastName')?.value,
      email: this.contractorForm.get('email')?.value,
      phone: this.contractorForm.get('phone')?.value,
    } : [] : false

    let jobCreateRequest = {}

    if (this.isExamplePrefilled) {
      jobCreateRequest = false
    } else {
      if (this.jobGeneralForm.invalid) {
        this.jobGeneralForm.markAllAsTouched();
        this.snackBar.open('Invalid fields, please revise the form and resubmit', '', {
          duration: 3000
        });
      }

      let servicesField: { id: any; }[] = []
      if (this.services.services.length !== 0) {
        this.services.services.forEach((element: any) => {
          servicesField.push({ "id": element["serviceID"] })
        })
      }

      let materialsField: { id: any, unitsUsed: any, pricePerUnit: any }[] = []
      if (this.materials.materials.length !== 0) {
        this.materials.materials.forEach((element: any) => {
          materialsField.push({
            "id": element["materialID"],
            "unitsUsed": element["unitsUsed"],
            "pricePerUnit": element["pricePerUnit"]
          });
        });
      }

      let contractorsField: { id: any; }[] = []
      if (this.contractors.contractors.length !== 0) {
        this.contractors.contractors.forEach((element: any) => {
          contractorsField.push({ "id": element["contractorID"] })
        });
      }

      jobCreateRequest = {
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
        materials: materialsField as [],
        flatfee: this.jobGeneralForm.get('flatfee')?.value,
        hourlyrate: this.jobGeneralForm.get('hourlyRate')?.value,
        minutesworked: this.jobGeneralForm.get('minutesWorked')?.value,
      }
    }

    const onboardingUpdateRequest = {
      customerRequest: customerCreateRequest,
      serviceRequest: serviceCreateRequest,
      materialRequest: materialCreateRequest,
      contractorRequest: contractorCreateRequest,
      isOnboarding: false,
      jobRequest: jobCreateRequest
    }

    this.updateOnboardingField(onboardingUpdateRequest)
  }

  onCancelOnboaring() {
    const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
      width: '500px',
      data: "cancel of the onboaring process? (All steps will be lost)"
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.navigateToPage('home');
      }
    });
  }

  updateOnboardingField(request: any) {
    //submits the data to save
    this.organizationService.updateOnboardingProcess(request).subscribe({
      next: (response) => {
        this.snackBar.open('Onboarding completed!', '', {
          duration: 3000
        });
        this.navigateToPage('update-payment');
      },
      error: (error) => {
      }
    });
  }
}
