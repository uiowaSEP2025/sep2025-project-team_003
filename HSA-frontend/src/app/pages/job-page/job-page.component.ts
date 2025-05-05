import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { JobService } from '../../services/job.service';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { MatTabChangeEvent, MatTabsModule } from '@angular/material/tabs';

@Component({
  selector: 'app-job-page',
  imports: [TableComponentComponent,
    MatButtonModule,
    MatIconModule,
    LoadingFallbackComponent,
    CommonModule,
    MatTabsModule],
  templateUrl: './job-page.component.html',
  styleUrl: './job-page.component.scss'
})
export class JobPageComponent implements OnInit {
  jobs: any = null;
  jobService: JobService
  selectedTab: "Created" | "In Progress" | "Completed" = "Created" // MAKE SURE TO UPDATE THIS IF WE ADD A NEW TAB!!!

  constructor(private router: Router, jobService: JobService) {
    this.jobService = jobService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  onTabChange(event: MatTabChangeEvent) {
      this.selectedTab = (event.tab.textLabel as "Created" | "In Progress" | "Completed");
    }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    const tabToApiMap: Record<typeof this.selectedTab, string> = {
      "Created": "created",
      "In Progress": "in-progress",
      "Completed": "completed"
    };

    const statusQuery: "created" | "in-progress" | "completed" = tabToApiMap[this.selectedTab] as "created" | "in-progress" | "completed";;
    console.log(statusQuery)
    this.jobService.getJob(statusQuery, { search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.jobs = response
      },
      error: (error) => {
      }
    })
  }

  redirectJobDetails(element: any) {
    this.router.navigate([`/job/${element.id}`])
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
