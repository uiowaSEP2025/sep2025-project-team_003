import { Component, Inject, ViewChild } from '@angular/core';
import { TableComponentComponent } from '../table-component/table-component.component';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface';

@Component({
  selector: 'app-onboarding-select-dialog-component',
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    TableComponentComponent,
    LoadingFallbackComponent
  ],
  templateUrl: './onboarding-select-dialog-component.component.html',
  styleUrl: './onboarding-select-dialog-component.component.scss'
})
export class OnboardingSelectDialogComponentComponent {
  checkedIds: number[] | null = null
  isNotSelectedItems: boolean = true
  isMaterial: boolean = false
  typeOfDialog: string = ''
  dialogData: any = null
  allDataEntries: any[] = []
  searchHint: string = '';
  headers: string[] = []
  templates: any
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
    public dialogRef: MatDialogRef<OnboardingSelectDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: AddSelectDialogData,
    public dialog: MatDialog,
  ) {
    this.isMaterial = this.data.typeOfDialog === 'material' ? true : false;
    this.typeOfDialog = this.data.typeOfDialog;
    this.headers = this.data.headers;
    this.materialInputFields = this.data.materialInputFields;
  }

  ngOnInit() {
    switch(this.typeOfDialog) {
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
    this.dialogData = { data: this.data.dialogData.contractors };
    this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
  }


  loadServicesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.dialogData = { data: this.data.dialogData.services };
    this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
  }

  loadMaterialsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.dialogData = { data: this.data.dialogData.materials };
    this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
  }

  loadCustomersToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.dialogData = { data: this.data.dialogData.customers} ;
    this.allDataEntries = [...new Set([...this.allDataEntries, ...this.dialogData.data])];
  }

  setSelectedCustomer(customers: number[]) {
    this.selectedCustomer = [...customers];
    this.selectedItems = this.selectedCustomer;
    this.selectedCustomerIsError = this.selectedCustomer === null ? true : false
    this.isNotSelectedItems = this.selectedCustomer === null ? true : false
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
      this.selectedMaterials.forEach((element: any) => {
        if (previousMaterialInputFields.some((item) => item.id === element)) {
          let specificEntry = previousMaterialInputFields.find((item) => item.id === element);
          this.materialInputFields.push({"id": element, "unitsUsed": specificEntry!["unitsUsed"], "pricePerUnit": specificEntry!["pricePerUnit"]});
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
      if (this.typeOfDialog === 'material') {
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

    this.dialogRef.close({
      selectedItems: this.typeOfDialog === 'customer' 
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

  getUnitsUsedValue(id: number): number | string {
    const entry = this.materialInputFields.find(item => item.id === id);
    return entry?.['unitsUsed'] ?? ''; 
  }

  getPricePerUnitValue(id: number): number | string {
    const entry = this.materialInputFields.find(item => item.id === id);
    return entry?.['pricePerUnit'] ?? ''; 
  }

  getButtonAction(): string {
    if (this.typeOfDialog === 'customer') {
      return this.data.dialogData === 0 ? 'select' : 'change';
    }
    return 'add';
  }
}
