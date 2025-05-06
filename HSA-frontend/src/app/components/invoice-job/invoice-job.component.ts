import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { MatTableModule } from '@angular/material/table';

interface Job {
  flatFee: number;
  hourlyRate: number;
  hoursWorked: number;
  totalCost: number;
  description: string; 
}

export interface Invoice {
  id: number;
  status: string;
  dueDate: string;
  issuanceDate: string;
  customer: string;
  taxAmount: string;
  taxPercent: string;
  grandTotal: string;
  jobs: Job[];
}

@Component({
  selector: 'app-invoice-job',
  imports: [MatTableModule],
  templateUrl: './invoice-job.component.html',
  styleUrl: './invoice-job.component.scss'
})
export class InvoiceJobComponent implements OnChanges{
  @Input() data!: Invoice
  displayedColumns = ["Description", "Flat Fee", "Hourly Rate", "Hours Worked", "Total Cost"]
  displayData: any | null = null;

  ngOnChanges(changes: SimpleChanges): void {
    if (this.data) {
      this.displayData = this.data.jobs.map((job: any) => (
        {"Flat Fee": job.flatFee,
         "Hourly Rate": job.hourlyRate,
         "Hours Worked": job.hoursWorked,
         "Total Cost": job.totalCost,
         "Description": job.description
        }

      ));
    }
  }
  
}
