import { Component, Inject, Input, OnInit, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { StringFormatter } from '../../utils/string-formatter';
import { MatButtonModule } from '@angular/material/button';
import { TableComponentComponent } from "../table-component/table-component.component";
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { AddSelectDialogData } from '../../interfaces/interface-helpers/addSelectDialog-helper.interface';
import { ServiceService } from '../../services/service.service';
import { MaterialService } from '../../services/material.service';
import { ContractorService } from '../../services/contractor.service';
import { ErrorHandlerService } from '../../services/error.handler.service';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';

@Component({
  selector: 'app-add-select-dialog-component',
  imports: [
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
  selectedItems: any = []
  isMaterial: boolean = false
  typeOfDialog: string = ''
  dialogData: any = null
  loadData: any
  setSelectedItems: any
  searchHint: string = '';
  headers: string[] = []
  materialInputFields: InputFieldDictionary[]
  setMaterialInputFields: any
  @ViewChild(TableComponentComponent) tableComponent!: TableComponentComponent;

  constructor(
    public dialogRef: MatDialogRef<AddSelectDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: AddSelectDialogData,
    stringFormatter: StringFormatter,
    private serviceService: ServiceService,
    private materialService: MaterialService,
    private contractorService: ContractorService,
    private errorHandler: ErrorHandlerService,
  ) {
    this.isMaterial = this.data.typeOfDialog === 'material' ? true : false
    this.typeOfDialog = this.data.typeOfDialog
    this.dialogData = this.data.dialogData,
    this.loadData = this.data.loadData
    this.setSelectedItems = this.data.setSelectedItems,
    this.searchHint = this.data.searchHint,
    this.headers = this.data.headers,
    this.materialInputFields = this.data.materialInputFields
    this.setMaterialInputFields = this.data.setMaterialInputFields
  }

  ngOnInit() {
    switch(this.typeOfDialog) {
      case 'service':
        this.loadServicesToTable('', 5, 0)
        break;
      case 'material':
        this.loadMaterialsToTable('', 5, 0)
        break;
      case 'contractor':
        this.loadContractorsToTable('', 5, 0)
        break;
    }
  }

  loadServicesToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.serviceService.getService({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.dialogData = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  loadMaterialsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.materialService.getMaterial({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.dialogData = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  loadContractorsToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.contractorService.getContractor({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.dialogData = response
      },
      error: (error) => {
        this.errorHandler.handleError(error)
      }
    })
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }

  onConfirm(): void {
    this.dialogRef.close(true);
  }

  getUnitsUsedValue(id: number): number | string {
    const entry = this.materialInputFields.find(item => item.id === id);
    return entry?.['unitsUsed'] ?? ''; 
  }

  getPricePerUnitValue(id: number): number | string {
    const entry = this.materialInputFields.find(item => item.id === id);
    return entry?.['pricePerUnit'] ?? ''; 
  }

  setMaterialInput(inputField: InputFieldDictionary[]) {
    this.materialInputFields = inputField
  }
}
