import { Component, ViewChild } from '@angular/core';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { ServiceService } from '../../services/service.service';
import { MaterialService } from '../../services/material.service';
import { CustomerService } from '../../services/customer.service';
import { JobService } from '../../services/job.service';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButton } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog } from '@angular/material/dialog';
import { AddConfirmDialogComponentComponent } from '../../components/add-confirm-dialog-component/add-confirm-dialog-component.component';
import { ContractorService } from '../../services/contractor.service';

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
  ],
  templateUrl: './onboarding-page.component.html',
  styleUrl: './onboarding-page.component.scss'
})
export class OnboardingPageComponent {
  serviceForm: FormGroup;
  materialForm: FormGroup;
  customerForm: FormGroup;
  contractorForm: FormGroup;
  firstService: any;
  firstCustomer: any;
  firstMaterial: any;
  firstContractor: any;
  @ViewChild('stepper') stepper!: MatStepper;

  constructor(
    private serviceFormBuilder: FormBuilder,
    private materialFormBuilder: FormBuilder,
    private customerFormBuilder: FormBuilder,
    private contractorFormBuilder: FormBuilder,
    private serviceService: ServiceService,
    private materialService: MaterialService,
    private customerService: CustomerService,
    private contractorService: ContractorService,
    private jobService: JobService,
    public dialog: MatDialog
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
      email: ['', Validators.required],
      phone: ['', Validators.required],
      note: ['', Validators.required]
    })

    this.contractorForm = this.contractorFormBuilder.group({
      firstName: [''],
      lastName: [''],
      email: [''],
      phone: [''],
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

  openPrefillDialog(type: string) {
    const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
      width: '300px',
      data: "prefill data"
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        switch (type) {
          case "service":
            this.serviceForm.setValue({
              serviceName: "Example Service",
              serviceDescription: "Example Service Description"
            });
            break;
          case "customer":
            this.customerForm.setValue({
              firstName: "First",
              lastName: "Last",
              email: "first.last@example.com",
              phone: "000-000-0000",
              note: "Example Note"
            });
            break;
          case "material":
            this.materialForm.setValue({
              materialName: "Example Material"
            });
            break;
          case "contractor":
            this.contractorForm.setValue({
              firstName: "FirstCon",
              lastName: "LastCon",
              email: "firstCon.lastCon@example.com",
              phone: "000-000-0000",
            });
            break;
        }
      }
    })
  }
}
