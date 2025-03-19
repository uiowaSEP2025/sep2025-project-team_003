import { Component, Input, OnInit } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { ContractorJSON, JobDisplayInterface, MaterialJSON, ServiceJSON } from '../../interfaces/api-responses/job.api.display.interface';
import { JobDataInterface } from '../../interfaces/api-responses/job.api.data.interface';

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
  imports: [MatTableModule],
  templateUrl: './job-display-table.component.html',
  styleUrl: './job-display-table.component.scss'
})

export class JobDisplayTableComponent  implements OnInit {
  @Input({ required: true }) dataSource!: JobDisplayInterface
  @Input({ required: true}) typeToDisplay: string = 'service'

  displayedServiceColumns: string[] = []
  displayedMaterialColumns: string[] = []
  displayedContractorColumns: string[] = []

  services!: ServiceJSON[]
  materials!: MaterialJSON[]
  contractors!: ContractorJSON[]
  displayServices!: ServiceRowItem[]
  displayMaterials!: MaterialRowItem[]
  displayContractors!: ContractorRowItem[]

  constructor () {}

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
    }
  }
}
