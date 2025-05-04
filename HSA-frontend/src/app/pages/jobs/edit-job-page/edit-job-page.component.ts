import { Component } from '@angular/core';
import { JobDataInterface } from '../../../interfaces/api-responses/job.api.data.interface';
import { JobService } from '../../../services/job.service';
import { ActivatedRoute, Router } from '@angular/router';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { JobDisplayTableComponent } from '../../../components/job-display-table/job-display-table.component';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { InputFieldDictionary } from '../../../interfaces/interface-helpers/inputField-row-helper.interface';
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { AddSelectDialogComponentComponent } from '../../../components/add-select-dialog-component/add-select-dialog-component.component';
import { MatDialog } from '@angular/material/dialog';
import { AddSelectDialogData } from '../../../interfaces/interface-helpers/addSelectDialog-helper.interface'
import { MatSnackBar } from '@angular/material/snack-bar';
import { StringFormatter } from '../../../utils/string-formatter';
import { UpdateConfirmDialogComponentComponent } from '../../../components/update-confirm-dialog-component/update-confirm-dialog-component.component';
import { RequestTrackerService } from '../../../utils/request-tracker';
import { take } from 'rxjs/operators';
import { StateList } from '../../../utils/states-list';

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
  jobID!: number | null
  jobData: JobDataInterface | null = null;
  customers: any
  services: any
  materials: any
  contractors: any
  allServices: any = []
  allMaterials: any = []
  allContractors: any = []
  selectedCustomer: number = 0
  selectedServices: any = []
  selectedMaterials: any = []
  selectedContractors: any = []
  deletedCustomers: any = []
  deletedJobServices: any = []
  deletedJobMaterials: any = []
  deletedJobContractors: any = []
  materialInputFields: InputFieldDictionary[] = []
  status: 'created' | 'in-progress' | 'completed' = 'created'
  customerID: number = 0
  description: string = ''
  address: string = ''
  city: string = ''
  state: string = ''
  zip: string = ''
  jobForm: FormGroup;
  states: any = []
  isUpdatedField: boolean = false

  constructor (
    private jobService: JobService,
    private stringFormatter: StringFormatter,
    private activatedRoute:ActivatedRoute,
    private router: Router,
    private tracker: RequestTrackerService,
    private jobFormBuilder: FormBuilder,
    private http: HttpClient,
    public dialog: MatDialog,
    private snackBar: MatSnackBar,
  ) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.jobID = Number(params.get('id'));
    })
    this.states = StateList.getStates()

    this.jobForm = this.jobFormBuilder.group({
      customerName: ['', Validators.required],
      jobStatus: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: ['', Validators.required],
      jobDescription: ['', Validators.required],
      requestorAddress: [''],
      requestorCity: [''],
      requestorZip: [''],
      requestorStateSelect: ['', Validators.required]
    }, { validators: this.dateValidator });
  }

  ngOnInit(): void {
    this.jobService.getSpecificJobData(this.jobID).subscribe(
      {next: (response) => {
        this.jobData = response;

        this.jobForm.setValue({
          customerName: this.jobData?.data.customerName,
          jobStatus: this.jobData?.data.jobStatus,
          startDate: new Date(this.jobData?.data.startDate),
          endDate: new Date(this.jobData?.data.endDate),
          jobDescription: this.jobData?.data.description,
          requestorAddress: this.jobData?.data.requestorAddress,
          requestorCity: this.jobData?.data.requestorCity,
          requestorZip: this.jobData?.data.requestorZip,
          requestorStateSelect: this.jobData?.data.requestorState,
        });

        this.customerID = this.jobData?.data.customerID;
        this.customers = this.jobData?.data.customerName;
        this.services = this.jobData.services;
        this.materials = this.jobData.materials;
        this.contractors = this.jobData.contractors;
        this.jobForm.markAllAsTouched();
      },
      error: (error) => {
      }}
    );
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

    dialogRef.afterClosed().subscribe((result:any) => {
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
        this.onChangeUpdateButton();
      }
    });
  }

  onChangeUpdateButton() {
    this.isUpdatedField = this.jobData?.data.jobStatus !== this.jobForm.get('jobStatus')?.value
      || this.stringFormatter.dateFormatter(new Date(this.jobData?.data.startDate as string)) !== this.stringFormatter.dateFormatter(this.jobForm.get('startDate')?.value)
      || this.stringFormatter.dateFormatter(new Date(this.jobData?.data.endDate as string)) !== this.stringFormatter.dateFormatter(this.jobForm.get('endDate')?.value)
      || this.jobData?.data.description !== this.jobForm.get('jobDescription')?.value
      || this.jobData?.data.requestorAddress !== this.jobForm.get('requestorAddress')?.value
      || this.jobData?.data.requestorCity !== this.jobForm.get('requestorCity')?.value
      || this.jobData?.data.requestorState !== this.jobForm.get('requestorStateSelect')?.value
      || this.jobData?.data.requestorZip !== this.jobForm.get('requestorZip')?.value
      || this.jobData?.data.customerName !== this.jobForm.get('customerName')?.value
      || this.selectedServices.length !== 0
      || this.deletedJobServices !== 0
      || this.selectedMaterials.length !== 0
      || this.deletedJobMaterials !== 0
      || this.selectedContractors.length !== 0
      || this.deletedJobContractors !== 0

    return this.isUpdatedField;
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

  onUpdateConfirmDialog() {
    const dialogRef = this.dialog.open(UpdateConfirmDialogComponentComponent, {
      data: "job updating"
    });

    dialogRef.afterClosed().subscribe((result:any) => {
      if (result) {
        this.onSubmit();
      }
    });
  }

  onSubmit() {
    let onSubmitSucessful = true;
    let errorMessage = '';

    if (this.jobForm.invalid) {
      this.snackBar.open('Invalid fields, please revise the form and resubmit', '', {
        duration: 3000
      });
    } else {
      //call edit job api
      const editJobRequestJson = {
        id: this.jobID,
        jobStatus: this.jobForm.get('jobStatus')?.value,
        startDate: this.stringFormatter.dateFormatter(this.jobForm.get('startDate')?.value),
        endDate: this.stringFormatter.dateFormatter(this.jobForm.get('endDate')?.value),
        description: this.jobForm.get('jobDescription')?.value,
        customerID: this.selectedCustomer === 0 ? this.customerID : this.selectedCustomer,
        city: this.jobForm.get('requestorCity')?.value,
        state: this.jobForm.get('requestorStateSelect')?.value,
        zip: this.jobForm.get('requestorZip')?.value,
        address: this.jobForm.get('requestorAddress')?.value
      };

      this.tracker.startRequest();
      this.jobService.editJob(editJobRequestJson).subscribe(
        {
          next: (response) => {
            onSubmitSucessful = true;
            this.tracker.endRequest();
          },
          error: (error) => {
            onSubmitSucessful = false;
            errorMessage = error.status + " " + error.statusText;
            this.tracker.endRequest();
          }
        }
      );

      //call delete on join relations
      let deletedServicesField: { id: any; } [] = [];
      this.deletedJobServices = Array.from(new Set(this.deletedJobServices))
      this.deletedJobServices.forEach((element: any) => {
        deletedServicesField.push({ "id": element });
      });

      const deleteJobServicesRequestJson = {
        type: 'service',
        id: this.jobID,
        deletedItems: { "jobServices" : deletedServicesField }
      };

      let deletedMaterialsField: { id: any; } [] = [];
      this.deletedJobMaterials = Array.from(new Set(this.deletedJobMaterials))

      this.deletedJobMaterials.forEach((element: any) => {
        deletedMaterialsField.push({ "id": element });
      });

      const deleteJobMaterialsRequestJson = {
        type: 'material',
        id: this.jobID,
        deletedItems: { "jobMaterials" : deletedMaterialsField }
      };

      let deletedContractorsField: { id: any; } [] = [];
      this.deletedJobContractors = Array.from(new Set(this.deletedJobContractors))
      this.deletedJobContractors.forEach((element: any) => {
        deletedContractorsField.push({ "id": element });
      });

      const deleteJobContractorsRequestJson = {
        type: 'contractor',
        id: this.jobID,
        deletedItems: { "jobContractors" : deletedContractorsField }
      };

      if (deletedServicesField.length !== 0) {
        this.tracker.startRequest();
        this.jobService.deleteJobJoin(deleteJobServicesRequestJson).subscribe(
          {
            next: (response) => {
              onSubmitSucessful = true;
              this.tracker.endRequest();
            },
            error: (error) => {
              onSubmitSucessful = false;
              errorMessage = error.status + " " + error.statusText;
              this.tracker.endRequest();
            }
          }
        );
      }

      if (deletedMaterialsField.length !== 0) {
        this.tracker.startRequest();
        this.jobService.deleteJobJoin(deleteJobMaterialsRequestJson).subscribe(
          {
            next: (response) => {
              onSubmitSucessful = true;
              this.tracker.endRequest();
            },
            error: (error) => {
              onSubmitSucessful = false;
              errorMessage = error.status + " " + error.statusText;
              this.tracker.endRequest();
            }
          }
        );
      }

      if (deletedContractorsField.length !== 0) {
        this.tracker.startRequest();
        this.jobService.deleteJobJoin(deleteJobContractorsRequestJson).subscribe(
          {
            next: (response) => {
              onSubmitSucessful = true;
              this.tracker.endRequest();
            },
            error: (error) => {
              onSubmitSucessful = false;
              errorMessage = error.status + " " + error.statusText;
              this.tracker.endRequest();
            }
          }
        );
      }

      //call create on join relations
      let selectedServicesField: { id: any; } [] = [];
      this.selectedServices.forEach((element: any) => {
        selectedServicesField.push({ "id": element });
      });

      const createJobServicesRequestJson = {
        type: 'service',
        id: this.jobID,
        addedItems: { "services" : selectedServicesField }
      };

      let selectedMaterialsField = this.selectedMaterials;
      const createJobMaterialsRequestJson = {
        type: 'material',
        id: this.jobID,
        addedItems: { "materials" : selectedMaterialsField }
      };

      let selectedContractorsField: { id: any; } [] = [];
      this.selectedContractors.forEach((element: any) => {
        selectedContractorsField.push({ "id": element });
      });

      const createJobContractorsRequestJson = {
        type: 'contractor',
        id: this.jobID,
        addedItems: { "contractors" : selectedContractorsField }
      };

      this.tracker.completionNotifier.pipe(take(1)).subscribe(() => {
        if (selectedServicesField.length !== 0) {
          this.tracker.startRequest();
          this.jobService.createJobJoin(createJobServicesRequestJson).subscribe(
            {
              next: (response) => {
                onSubmitSucessful = true;
                this.tracker.endRequest();
              },
              error: (error) => {
                onSubmitSucessful = false;
                errorMessage = error.status + " " + error.statusText;
                this.tracker.endRequest();
              }
            }
          );
        }
      });

      this.tracker.completionNotifier.pipe(take(1)).subscribe(() => {
        if (selectedMaterialsField.length !== 0) {
          this.tracker.startRequest();
          this.jobService.createJobJoin(createJobMaterialsRequestJson).subscribe(
            {
              next: (response) => {
                onSubmitSucessful = true;
                this.tracker.endRequest();
              },
              error: (error) => {
                onSubmitSucessful = false;
                errorMessage = error.status + " " + error.statusText;
                this.tracker.endRequest();
              }
            }
          );
        }
      })

      this.tracker.completionNotifier.pipe(take(1)).subscribe(() => {
        if (selectedContractorsField.length !== 0) {
          this.tracker.startRequest();
          this.jobService.createJobJoin(createJobContractorsRequestJson).subscribe(
            {
              next: (response) => {
                onSubmitSucessful = true;
                this.tracker.endRequest();
              },
              error: (error) => {
                onSubmitSucessful = false;
                errorMessage = error.status + " " + error.statusText;
                this.tracker.endRequest();
              }
            }
          );
        }
      })

      this.tracker.completionNotifier.pipe(take(1)).subscribe(() => {
        //Wait for all requests to make through
        if (onSubmitSucessful === true) {
          this.snackBar.open('Job edit successfully', '', {
            duration: 3000
          });
        this.navigateToPage('jobs') }
        else {
          this.snackBar.open('There is an error in the server, please try again later. Error: ' + errorMessage, '', {
            duration: 3000
          });
        }
      });

      this.resetAllParameters()
    }
  }

  resetAllParameters() {
    this.isUpdatedField = false;
    this.selectedServices = [];
    this.selectedMaterials = [];
    this.selectedContractors = [];
    this.deletedJobServices = [];
    this.deletedJobMaterials = [];
    this.deletedJobContractors = []
  }
}
