import { Component, Inject, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { TableComponentComponent } from "../table-component/table-component.component";
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface';
import { ServiceService } from '../../services/service.service';
import { MaterialService } from '../../services/material.service';
import { ContractorService } from '../../services/contractor.service';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';
import { CustomerService } from '../../services/customer.service';
import { JobTemplateService } from '../../services/jobTemplate.service';
import { ApplyTemplateConfirmDialogComponentComponent } from '../apply-template-confirm-dialog-component/apply-template-confirm-dialog-component.component';
import { CommonModule } from '@angular/common';
import { JobService } from '../../services/job.service';

@Component({
  selector: 'app-add-select-dialog-component',
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    TableComponentComponent,
    LoadingFallbackComponent
],
  templateUrl: './add-select-dialog-component.component.html',
  styleUrl: './add-select-dialog-component.component.scss'
})
export class AddSelectDialogComponentComponent {
  checkedIds: number[] | null = null
  isNotSelectedItems: boolean = true
  isMaterial: boolean = false
  typeOfDialog: string = ''
  dialogData: any = null
  allDataEntries: any[] = []
  searchHint: string = '';
  headers: string[] = []
  templates: any
  jobs: any
  customers: any
  services: any
  materials: any
  contractors: any
  tableItems: any
  selectedItems: any = []
  selectedTemplate: any = []
  selectedTemplateIsError: boolean = false
  selectedCustomer: any = []
  selectedCustomerIsError: boolean = false
  selectedJob: any = []
  selectedJobIsError: boolean = false
  selectedServices: any = []
  selectedServicesIsError: boolean = false
  selectedMaterials: any = []
  selectedMaterialsIsError: boolean = false
  selectedContractors: any = []
  selectedContractorsIsError: boolean = false
  materialInputFields: InputFieldDictionary[]
  setMaterialInputFields: any
  @ViewChild(TableComponentComponent) tableComponent!: TableComponentComponent;

  constructor(
    public dialogRef: MatDialogRef<AddSelectDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: AddSelectDialogData,
    public dialog: MatDialog,
    private jobService: JobService,
    private customerService: CustomerService,
    private serviceService: ServiceService,
    private materialService: MaterialService,
    private contractorService: ContractorService,
    private jobTemplateService: JobTemplateService,
  ) {
    this.isMaterial = this.data.typeOfDialog === 'material' ? true : false;
    this.typeOfDialog = this.data.typeOfDialog;
    this.dialogData = this.data.dialogData;
    this.searchHint = this.data.searchHint;
    this.headers = this.data.headers;
    this.materialInputFields = this.data.materialInputFields;
  }

  ngOnInit() {
    switch(this.typeOfDialog) {
      case 'job':
        this.loadJobsToTable('', 5, 0);
        break;
      case 'customer':
        this.loadCustomersToTable('', 5, 0);
        break;
      case 'service':
        this.loadServicesToTable('', 5, 0);
        break;
      case 'material':
        this.loadMaterialsToTable('', 5, 0);
        break;
      case 'contractor':
        this.loadContractorsToTable('', 5, 0);
        break;
      case 'template':
        this.loadJobTemplatesToTable('', 5, 0)
    }
  }

  getIDsFromData(items: any, key: string): number[] {
    let IDs: number[] = [];

    items.forEach((element: { [x: string]: number; }) => {
      IDs.push(element[key]);
    });
    return IDs;
  }

  loadContractorsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.contractorService.getExcludedContractor({ excludeIDs: this.getIDsFromData(this.data.dialogData.contractors, 'contractorID'), search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.dialogData = response;
        this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
      },
      error: (error) => {
      }
    });
  }


  loadServicesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.serviceService.getExcludedService({ excludeIDs: this.getIDsFromData(this.data.dialogData.services, 'serviceID'), search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.dialogData = response;
        this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
      },
      error: (error) => {
      }
    });
  }

  loadMaterialsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.materialService.getExcludedMaterial({ excludeIDs: this.getIDsFromData(this.data.dialogData.materials, 'materialID'), search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.dialogData = response
        this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
      },
      error: (error) => {
      }
    });
  }

  loadCustomersToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.customerService.getExcludedCustomer({ excludeIDs: [this.data.dialogData], search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.dialogData = response;
        this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
      },
      error: (error) => {
      }
    });
  }

  loadJobsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.jobService.getExcludedJob({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.dialogData = response;
        this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
      },
      error: (error) => {
      }
    })
  }

  loadJobTemplatesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.jobTemplateService.getJobTemplate({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.dialogData = response;
        this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
      },
      error: (error) => {
      }
    });
  }

  setSelectedCustomer(customers: number[]) {
    this.selectedCustomer = [...customers];
    this.selectedItems = this.selectedCustomer;
    this.selectedCustomerIsError = this.selectedCustomer === null ? true : false
    this.isNotSelectedItems = this.selectedCustomer === null ? true : false
  }

  setSelectedJob(jobs: number[]) {
    this.selectedJob = [...jobs];
    this.selectedItems = this.selectedJob;
    this.selectedJobIsError= this.selectedJob === null ? true : false
    this.isNotSelectedItems = this.selectedJob === null ? true : false
  }

  setSelectedJobTemplate(templates: number[]) {
    this.selectedTemplate = [...templates];
    this.selectedItems = this.selectedTemplate;
    this.selectedTemplateIsError = this.selectedTemplate === null ? true : false
    this.isNotSelectedItems = this.selectedTemplate === null ? true : false
  }

  setSelectedServices(services: number[]) {
    this.selectedServices = [...services];
    this.selectedItems = this.selectedServices;
    this.selectedServicesIsError = this.selectedServices.length === 0 ? true : false;
    this.isNotSelectedItems = this.selectedServices.length === 0 ? true : false;

  }

  setSelectedMaterials(materials: number[]) {
    this.selectedMaterials = [...materials];
    this.selectedItems = this.selectedMaterials;
    this.selectedMaterialsIsError = this.selectedMaterials.length === 0 ? true : false;
    this.isNotSelectedItems = this.selectedMaterials.length === 0 ? true : false;

    if (this.selectedMaterialsIsError === false) {
      let previousMaterialInputFields = this.materialInputFields;
      this.materialInputFields = [];
      console.log(this.selectedMaterials);
      this.selectedMaterials.forEach((element: any) => {
        if (previousMaterialInputFields.some((item) => item.id === element)) {
          let specificEntry = previousMaterialInputFields.find((item) => item.id === element);
          this.materialInputFields.push({"id": element, "unitsUsed": specificEntry!["unitsUsed"], "materialDescription": specificEntry!['description'], "pricePerUnit": specificEntry!["pricePerUnit"]});
        } else {
          this.materialInputFields.push({"id": element, "unitsUsed": 0, "pricePerUnit": 0.00});
        }

      });
    } else {
      this.materialInputFields = [];
    }
  }

  setSelectedContractors(contractors: number[]) {
    this.selectedContractors = [...contractors];
    this.selectedItems = this.selectedContractors;
    this.selectedContractorsIsError = this.selectedContractors.length === 0 ? true : false;
    this.isNotSelectedItems = this.selectedContractors.length === 0 ? true : false;
  }

  setMaterialInput(inputField: InputFieldDictionary[]) {
    this.materialInputFields = inputField;
  }

  onCancel(): void {
    this.dialogRef.close([]);
  }

  onConfirm(): void {
    let itemsInfo: any[] = [];
    this.selectedItems.forEach((element : number) => {
      if (this.typeOfDialog === 'template') {
        const secondDialogRef = this.dialog.open(ApplyTemplateConfirmDialogComponentComponent, {
          width: 'auto',
          maxWidth: '90vw',
          height: 'auto',
          maxHeight: '90vh',
          data: element,
          disableClose: false
        });

        secondDialogRef.afterClosed().subscribe(result => {
          if (result !== false) {
            itemsInfo.push(result)
            this.dialogRef.close({
              selectedItems: itemsInfo
            })
          }
        })
      }
      else if (this.typeOfDialog === 'material') {
        let materialEntry = this.allDataEntries.filter((item: { [x: string]: number; }) => item['id'] === element)[0];
        let materialInputEntry = this.materialInputFields.filter((item) => item['id'] === element)[0];
        itemsInfo.push(
          { id: 0,
            materialID: materialEntry['id'],
            materialName: materialEntry['material_name'],
            unitsUsed: materialInputEntry['unitsUsed'],
            pricePerUnit: materialInputEntry['pricePerUnit']
          }
        );
      } else {
        itemsInfo.push(this.allDataEntries.filter((item: { [x: string]: number; }) => item['id'] === element)[0]);
      }
    });

    if (this.typeOfDialog !== 'template') {
      this.dialogRef.close({
        selectedItems: this.typeOfDialog === 'job'
          ? this.selectedJob[0]
           :this.typeOfDialog === 'customer'
            ? this.selectedCustomer[0]
            : this.typeOfDialog === 'service'
              ? this.selectedServices
              : this.typeOfDialog === 'contractor'
                ? this.selectedContractors
                : this.materialInputFields,
          itemsInfo: itemsInfo
        }
      );
    }
  }

  getUnitsUsedValue(id: number): number | string {
    const entry = this.materialInputFields.find(item => item.id === id);
    return entry?.['unitsUsed'] ?? '';
  }

  getPricePerUnitValue(id: number): number | string {
    const entry = this.materialInputFields.find(item => item.id === id);
    return entry?.['pricePerUnit'] ?? '';
  }

  getButtonAction(): string {
    if (this.typeOfDialog === 'template') {
      return 'apply';
    }
    if (this.typeOfDialog === 'customer' || this.typeOfDialog === 'job') {
      return this.data.dialogData === 0 ? 'select' : 'change';
    }
    return 'add';
  }
}
