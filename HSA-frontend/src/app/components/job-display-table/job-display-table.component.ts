import { Component, Input, OnInit } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { ContractorJSON, JobDisplayInterface, MaterialJSON, ServiceJSON } from '../../interfaces/api-responses/job.api.display.interface';
import { MatIcon } from '@angular/material/icon';
import { DeleteDialogComponentComponent } from '../delete-dialog-component/delete-dialog-component.component';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ErrorHandlerService } from '../../services/error.handler.service';

interface ServiceRowItem {
  "Service ID": string,
  "Service Name": string,
  "Service Description": string
}

interface MaterialRowItem {
  "Material ID": string,
  "Material Name": string,
  "Units Used": string,
  "Price Per Unit": string
}

interface ContractorRowItem {
  "Contractor ID": string,
  "Contractor Name": string,
  "Contractor Phone No": string,
  "Contractor Email": string
}

@Component({
  selector: 'app-job-display-table',
  imports: [MatTableModule, MatIcon],
  templateUrl: './job-display-table.component.html',
  styleUrl: './job-display-table.component.scss'
})

export class JobDisplayTableComponent  implements OnInit {
  @Input({ required: true }) dataSource!: JobDisplayInterface
  @Input({ required: true}) typeToDisplay: string = 'service'
  @Input() isEditRow: boolean = false
  @Input() popOutEntry!: (typeOfTable: string, data: any, joinRelationID: any) => any
  @Input() listOfTable: [] = []

  displayedServiceColumns: string[] = []
  displayedMaterialColumns: string[] = []
  displayedContractorColumns: string[] = []

  services!: ServiceJSON[]
  materials!: MaterialJSON[]
  contractors!: ContractorJSON[]
  displayServices!: ServiceRowItem[]
  displayMaterials!: MaterialRowItem[]
  displayContractors!: ContractorRowItem[]

  constructor (public dialog: MatDialog, private snackBar: MatSnackBar, private errorHandler: ErrorHandlerService) {}

  ngOnInit(): void {
    if (this.typeToDisplay === "service") {
      this.displayServices = this.dataSource.services.map(
        (service) => ({
          "Service ID": service.serviceID,
          "Service Name": service.serviceName,
          "Service Description": service.serviceDescription
        })
      )
      
      this.displayedServiceColumns = ["Service ID", "Service Name", "Service Description"]
      this.displayedServiceColumns = this.isEditRow === true ? [...this.displayedServiceColumns, "Actions"] : this.displayedServiceColumns
      
    }
    else if (this.typeToDisplay === "material") {
      this.displayMaterials = this.dataSource.materials.map(
        (material) => ({
          "Material ID": material.materialID,
          "Material Name": material.materialName,
          "Units Used": material.unitsUsed,
          "Price Per Unit": "$" + material.pricePerUnit
        })
      )

      this.displayedMaterialColumns = ["Material ID", "Material Name", "Units Used", "Price Per Unit"]
      this.displayedMaterialColumns = this.isEditRow === true ? [...this.displayedMaterialColumns, "Actions"] : this.displayedMaterialColumns
    }
    else if (this.typeToDisplay === "contractor") {
      this.displayContractors = this.dataSource.contractors.map(
        (contractor) => ({
          "Contractor ID": contractor.contractorID,
          "Contractor Name": contractor.contractorName,
          "Contractor Phone No": contractor.contractorPhoneNo,
          "Contractor Email": contractor.contractorEmail
        })
      )
      
      this.displayedContractorColumns = ["Contractor ID", "Contractor Name", "Contractor Phone No", "Contractor Email"]
      this.displayedContractorColumns = this.isEditRow === true ? [...this.displayedContractorColumns, "Actions"] : this.displayedContractorColumns
    }
  }

  openDeleteDialog(args: any, typeOfTable: string) {
    const dialogRef = this.dialog.open(DeleteDialogComponentComponent, {
      width: '300px',
      data: args
    });

    setTimeout(() => {
      document.getElementById('modal')?.removeAttribute('aria-hidden');
    }, 10);

    switch (typeOfTable) {
      case 'service': {
        dialogRef.afterClosed().subscribe(result => {
          if (result) {
            let jobServiceID = this.dataSource.services.filter((item: { serviceID: any; }) => item.serviceID === args["Service ID"])[0] as any
            this.popOutEntry(typeOfTable, args, jobServiceID.id)
            this.displayServices = this.dataSource.services?.map(
              (service) => ({
                "Service ID": service.serviceID,
                "Service Name": service.serviceName,
                "Service Description": service.serviceDescription
              })
            )
          }
        })
        break;
      }

      case 'material': {
        dialogRef.afterClosed().subscribe(result => {
          if (result) {
            let jobMaterialID = this.dataSource.materials.filter((item: { materialID: any; }) => item.materialID === args["Material ID"])[0] as any
            this.popOutEntry(typeOfTable, args, jobMaterialID.id)
            this.displayMaterials = this.dataSource.materials.map(
              (material) => ({
                "Material ID": material.materialID,
                "Material Name": material.materialName,
                "Units Used": material.unitsUsed,
                "Price Per Unit": "$" + material.pricePerUnit
              })
            )
          }
        })
        break;
      }

      case 'contractor': {
        dialogRef.afterClosed().subscribe(result => {
          if (result) {
            let jobContractorID = this.dataSource.contractors.filter((item: { contractorID: any; }) => item.contractorID === args["Contractor ID"])[0] as any
            this.popOutEntry(typeOfTable, args, jobContractorID.id)
            this.displayContractors = this.dataSource.contractors.map(
              (contractor) => ({
                "Contractor ID": contractor.contractorID,
                "Contractor Name": contractor.contractorName,
                "Contractor Phone No": contractor.contractorPhoneNo,
                "Contractor Email": contractor.contractorEmail
              })
            )
          }
        })
        break;
      }
    }
  }
}
