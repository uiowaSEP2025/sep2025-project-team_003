import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StringFormatter } from '../../utils/string-formatter';
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatError, MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { LoadingFallbackComponent } from "../../components/loading-fallback/loading-fallback.component";
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { JobService } from '../../services/job.service';
import { StateList } from '../../utils/states-list';
import { MatCardModule } from '@angular/material/card';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatDialog } from '@angular/material/dialog';
import { JobDisplayTableComponent } from "../../components/job-display-table/job-display-table.component";
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface';
import { AddSelectDialogComponentComponent } from '../../components/add-select-dialog-component/add-select-dialog-component.component';
import { AddConfirmDialogComponentComponent } from '../../components/add-confirm-dialog-component/add-confirm-dialog-component.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CreateTemplateConfirmDialogComponentComponent } from '../../components/create-template-confirm-dialog-component/create-template-confirm-dialog-component.component';
import { JobTemplateService } from '../../services/jobTemplate.service';
import { currencyValidator } from '../../utils/currency-validator';

@Component({
  selector: 'app-create-job-page',
  imports: [
    CommonModule,
    MatButtonModule,
    MatError,
    FormsModule,
    MatFormFieldModule,
    MatCardModule,
    MatExpansionModule,
    MatSelectModule,
    LoadingFallbackComponent,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatDatepickerModule,
    JobDisplayTableComponent
  ],
  providers: [
    provideNativeDateAdapter()
  ],
  templateUrl: './create-job-page.component.html',
  styleUrl: './create-job-page.component.scss'
})

export class CreateJobPageComponent {
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
  description: string = ''
  address: string = ''
  city: string = ''
  state: string = ''
  zip: string = ''
  jobForm: FormGroup;
  states: any = []
  isUpdatedField: boolean = false
  isAllowedTemplate: boolean = false

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    public dialog: MatDialog,
    private jobService: JobService,
    private jobTemplateService: JobTemplateService,
    private stringFormatter: StringFormatter,
    private jobFormBuilder: FormBuilder,
    private snackBar: MatSnackBar,
  ) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.jobID = Number(params.get('id'));
    })
    this.states = StateList.getStates()

    this.jobForm = this.jobFormBuilder.group({
      customerName: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: ['', Validators.required],
      requestorAddress: ['', Validators.required],
      requestorCity: ['', Validators.required],
      requestorZip: ['', Validators.required],
      requestorStateSelect: ['', Validators.required],
      jobDescription: ['', Validators.required],
      flatfee: ['0.00', [Validators.required, currencyValidator()]],
      hourlyRate: ['0.00', [Validators.required, currencyValidator()]],
      minutesWorked: ['', [Validators.required, Validators.min(0)]],
    }, { validators: this.dateValidator });

    this.services = { "services": [] };
    this.materials = { "materials": [] };
    this.contractors = { "contractors": [] };
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

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }

  openApplyTemplateDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'template',
      dialogData: this.customerID,
      searchHint: 'Search by template name',
      headers: ['Description', 'Name'],
      materialInputFields: this.materialInputFields,
    };

    const firstDialogRef = this.dialog.open(AddSelectDialogComponentComponent, {
      width: 'auto',
      maxWidth: '90vw',
      height: 'auto',
      maxHeight: '90vh',
      data: dialogData,
      disableClose: true,
    });

    firstDialogRef.afterClosed().subscribe(result => {
      if (result.length !== 0) {
        let data = result.selectedItems[0];

        this.jobForm.patchValue({
          jobDescription: data.jobDescription
        });

        this.services.services = []
        data.services.services.forEach((element: { [x: string]: any; }) => {
          this.services = { services: [...this.services.services, element] };
        });

        this.selectedServices = result.selectedItems;

        this.materials.materials = []
        data.materials.materials.forEach((element: any) => {
          this.materials = { materials: [...this.materials.materials, element] };
        });

        this.selectedMaterials = result.selectedItems;
        this.onChangeUpdateButton();

        this.snackBar.open('Job template applied successfully', '', {
          duration: 3000
        });
        this.isAllowedTemplate = false
      }
    })
  }


  openAddCustomerDialog() {
    const dialogData: AddSelectDialogData = {
      typeOfDialog: 'customer',
      dialogData: this.customerID,
      searchHint: 'Search by customer name',
      headers: ['First Name', 'Last Name', 'Email', 'Phone No'],
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
        this.jobForm.controls['customerName'].setValue(customerEntry.first_name + " " + customerEntry.last_name)
        this.customerID = customerEntry.id;
        this.selectedCustomer = customerEntry.id

        this.onChangeUpdateButton()
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
        this.onChangeUpdateButton()
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

    dialogRef.afterClosed().subscribe((result: any) => {
      if (result.length !== 0) {
        result.itemsInfo.forEach((element: any) => {
          this.materials = { materials: [...this.materials.materials, element] };
        });

        this.selectedMaterials = result.selectedItems;
        this.onChangeUpdateButton();
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

    dialogRef.afterClosed().subscribe((result: any) => {
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
        this.onChangeUpdateButton();
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
        this.onChangeUpdateButton();
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
        this.onChangeUpdateButton();
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
        this.onChangeUpdateButton();
        return this.contractors;
      }
    };

  }

  onChangeUpdateButton() {
    this.isUpdatedField = this.jobForm.get('startDate')?.value
      || this.jobForm.get('endDate')?.value
      || this.jobForm.get('jobDescription')?.value
      || this.jobForm.get('requestorAddress')?.value
      || this.jobForm.get('requestorCity')?.value
      || this.jobForm.get('requestorStateSelect')?.value
      || this.jobForm.get('requestorZip')?.value
      || this.jobForm.get('customerName')?.value
      || this.selectedServices.length !== 0
      || this.deletedJobServices !== 0
      || this.selectedMaterials.length !== 0
      || this.deletedJobMaterials !== 0
      || this.selectedContractors.length !== 0
      || this.deletedJobContractors !== 0

    this.isAllowedTemplate = this.isUpdatedField

    return this.isUpdatedField;
  }

  onCreateConfirmDialog(type: string) {
    if (type === 'job') {
      const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
        data: "job creation"
      });

      dialogRef.afterClosed().subscribe((result: any) => {
        if (result) {
          this.onSubmit();
        }
      });
    } else if (type === 'template') {
      const templateCreateDialogData = {
        description: this.jobForm.get('jobDescription')?.value,
        services: this.services,
        materials: this.materials
      }

      const dialogRef = this.dialog.open(CreateTemplateConfirmDialogComponentComponent, {
        width: 'auto',
        maxWidth: '90vw',
        height: 'auto',
        maxHeight: '90vh',
        data: templateCreateDialogData,
      });

      dialogRef.afterClosed().subscribe(result => {
        if (result !== false) {

          let serviceFields: { id: any; }[] = []
          result.services.services.forEach((element: any) => {
            serviceFields.push({ "id": element["serviceID"] })
          });

          let materialsField: { id: any, unitsUsed: any, pricePerUnit: any }[] = []
          result.materials.materials.forEach((element: any) => {
            materialsField.push({
              "id": element["materialID"],
              "unitsUsed": element["unitsUsed"],
              "pricePerUnit": element["pricePerUnit"]
            })
          })

          const createTemplateRequest = {
            description: result.description,
            name: result.name,
            services: serviceFields as [],
            materials: materialsField as []
          }

          this.jobTemplateService.createJobTemplate(createTemplateRequest).subscribe({
            next: (response) => {
              this.snackBar.open('Job template create successfully', '', {
                duration: 3000
              });
              this.isAllowedTemplate = false
            },
            error: (error) => {
            }
          })
        }
      })
    }
  }

  onSubmit() {
    if (this.jobForm.invalid) {
      this.jobForm.markAllAsTouched();
      this.snackBar.open('Invalid fields, please revise the form and resubmit', '', {
        duration: 3000
      });
    }

    let servicesField: { id: any; }[] = []
    this.services.services.forEach((element: any) => {
      servicesField.push({ "id": element["serviceID"] })
    })



    let materialsField: { id: any, unitsUsed: any, pricePerUnit: any }[] = []
    this.materials.materials.forEach((element: any) => {
      materialsField.push({
        "id": element["materialID"],
        "unitsUsed": element["unitsUsed"],
        "pricePerUnit": element["pricePerUnit"]
      })
    })


    let contractorsField: { id: any; }[] = []
    this.contractors.contractors.forEach((element: any) => {
      contractorsField.push({ "id": element["contractorID"] })
    })

    const requestJson = {
      jobStatus: this.status,
      startDate: this.stringFormatter.dateFormatter(this.jobForm.get('startDate')?.value),
      endDate: this.stringFormatter.dateFormatter(this.jobForm.get('endDate')?.value),
      description: this.jobForm.get('jobDescription')?.value,
      customerID: this.selectedCustomer,
      city: this.jobForm.get('requestorCity')?.value,
      state: this.jobForm.get('requestorStateSelect')?.value,
      zip: this.jobForm.get('requestorZip')?.value,
      address: this.jobForm.get('requestorAddress')?.value,
      contractors: contractorsField as [],
      services: servicesField as [],
      materials: materialsField as [],
      flatfee: this.jobForm.get('flatfee')?.value,
      hourlyRate: this.jobForm.get('hourlyRate')?.value,    
      minutesWorked: this.jobForm.get('minutesWorked')?.value,    
    }

    this.jobService.createJob(requestJson).subscribe(
      {
        next: (response) => {
          this.snackBar.open('Job create successfully', '', {
            duration: 3000
          });
          this.router.navigate(['/jobs']);
        },
        error: (error) => {
        }
      }
    )
    return;
  }
}
