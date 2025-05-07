import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { StringFormatter } from '../../utils/string-formatter';

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
  url: string;
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

  constructor (private formatter: StringFormatter) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (this.data) {
      console.log(this.data)
      this.displayData = this.data.jobs.map((job: any) => (
        {"Flat Fee": this.formatter.formatCurrency(job.flatFee),
         "Hourly Rate": this.formatter.formatCurrency(job.hourlyRate),
         "Hours Worked": job.hoursWorked,
         "Total Cost": job.totalCost,
         "Description": job.description
        }

      ));

      this.displayData.push({"Flat Fee": "",
        "Hourly Rate": "",
        "Hours Worked": "",
        "Total Cost": this.formatter.formatTaxPercent(this.data.taxPercent),
        "Description": "Tax Percent"
       })
       this.displayData.push({"Flat Fee": "",
        "Hourly Rate": "",
        "Hours Worked": "",
        "Total Cost": this.formatter.formatCurrency(this.data.taxAmount),
        "Description": "Tax Amount"
       })
       this.displayData.push({"Flat Fee": "",
        "Hourly Rate": "",
        "Hours Worked": "",
        "Total Cost": this.formatter.formatCurrency(this.data.grandTotal),
        "Description": "Grand Total"
       })

    }
  }
  
}
