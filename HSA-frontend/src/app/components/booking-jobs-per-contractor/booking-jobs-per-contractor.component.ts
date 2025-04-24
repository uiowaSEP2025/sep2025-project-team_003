import { Component, Inject, OnInit } from '@angular/core';
import { TableComponentComponent } from '../table-component/table-component.component';
import JobSimplified from '../../interfaces/jobData.interface';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { JobService } from '../../services/job.service';
import { TableApiResponse } from '../../interfaces/api-responses/table.api.interface';
import { MatButtonModule } from '@angular/material/button';

interface dialogInput {
  contractorId: number
}

@Component({
  selector: 'app-booking-jobs-per-contractor',
  imports: [TableComponentComponent, MatButtonModule, MatDialogModule],
  templateUrl: './booking-jobs-per-contractor.component.html',
  styleUrl: './booking-jobs-per-contractor.component.scss'
})
export class BookingJobsPerContractorComponent implements OnInit {
  jobData: TableApiResponse<JobSimplified> | null = null
  totalCount:number = 0
  ids = []
  ngOnInit(): void {
    this.loadData("", 5, 0)
  }
  
  constructor(@Inject(MAT_DIALOG_DATA) public data: dialogInput, 
  private jobservice: JobService,
  private dialogRef: MatDialogRef<BookingJobsPerContractorComponent>) {} //this.data is the data
  


  loadData(search: string, pageSize: number, offSet: number) { 
    const contractorId = this.data.contractorId
      this.jobservice.getJobsByContractor(contractorId, search, pageSize, offSet).subscribe({
      next: (res) => {
        this.jobData = res
        console.log(this.jobData)
      }
    })
  }

  acceptSelection() {
    this.dialogRef.close(this.ids[0]);
  }

  closeDialog() {
    this.dialogRef.close(null);
  }
  
}
