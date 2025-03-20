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
import { MatError, MatFormFieldModule, MatLabel } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { LoadingFallbackComponent } from "../../components/loading-fallback/loading-fallback.component";
import { ServiceService } from '../../services/service.service';
import { MaterialService } from '../../services/material.service';
import { ContractorService } from '../../services/contractor.service';
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';

export interface DateRange {
  startDate: FormControl<Date | null>;
  endDate: FormControl<Date | null>;
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
    MatLabel,
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
  comtractors: any
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
  materialForm: FormGroup;
  @ViewChild(InvoiceDatePickerComponent) datePicker!: InvoiceDatePickerComponent;

  readonly range: FormGroup<DateRange> = new FormGroup({
    startDate: new FormControl<Date | null>(null),
    endDate: new FormControl<Date | null>(null),
  });

  constructor(
    private customerService: CustomerService, 
    private router: Router, 
    private errorHandler: ErrorHandlerService,
    private serviceService: ServiceService,
    private materialService: MaterialService,
    private contractorService: ContractorService,
    private stringFormatter: StringFormatter, 
    private materialFormBuilder: FormBuilder
  ) { 
    this.materialForm = this.materialFormBuilder.group({
      unitsUsed: [0, Validators.required],
      pricePerUnit: [0.00, [Validators.required]],
    });
  }

  ngOnInit(): void {
    this.loadCustomersToTable("", 5, 0);
  }

  isDateSelectVisible = () => (!(this.status === 'created'))

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
        console.log(this.services)
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
        console.log(this.materials)
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
    } else {
      this.selectedMaterials = []
      this.materials = { data: [], totalCount: 0 }
      this.selectedCustomersIsError = true
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

  // onSubmit() {
  // if (this.registrationForm.invalid) {
  //   this.registrationForm.markAllAsTouched();
  //   return;
  // } else {
  // }
  //   let validDates: any
  //   if (this.isDateSelectVisible()) {
  //     validDates = this.datePicker.validate()
  //   }
  //   if (this.selectedCustomers.length === 0) {
  //     this.selectedCustomersIsError = true
  //     return;
  //   }
  //   if (this.selectedQuotes.length === 0) {
  //     const quotesTableVisible = this.selectedCustomers.length !== 0
  //     if (quotesTableVisible) {
  //       this.selectedQuotesIsError = true
  //     }
  //     return;
  //   }
    
  //   if (this.isDateSelectVisible() && !validDates) {
  //     return;
  //   }
  //   const json = {
  //     customerID: this.selectedCustomers[0],
  //     quoteIDs: this.selectedQuotes,
  //     status: this.status,
  //     issuedDate: this.stringFormatter.dateFormatter(this.range.controls.issued.value),
  //     dueDate: this.stringFormatter.dateFormatter(this.range.controls.due.value)
  //   }
  //   this.invoiceService.createInvoice(json).subscribe(
  //     {
  //       next: (response) => {
  //         this.router.navigate(['/invoices']);
  //       },
  //       error: (error) => {
  //         this.errorHandler.handleError(error)
  //       }
  //     }
  //   )
  //   return;
  // }
}
