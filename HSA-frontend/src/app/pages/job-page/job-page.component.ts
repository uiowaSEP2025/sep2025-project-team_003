import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { JobService } from '../../services/job.service';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { MatTabChangeEvent, MatTabsModule } from '@angular/material/tabs';
import { TableApiResponse } from '../../interfaces/api-responses/table.api.interface';

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
  private defaultSearch = ""
  private defaultPageSize = 5
  private defaultOffset = 0

  jobService: JobService
  selectedTab: "Created" | "In Progress" | "Completed" = "Created" // MAKE SURE TO UPDATE THIS IF WE ADD A NEW TAB!!!
  tabStates: Record<"Created" | "In Progress" | "Completed", {
    search: string;
    pagesize: number;
    offset: number;
    data: TableApiResponse<any>;
  }> = {
      Created: { search: this.defaultSearch, pagesize: this.defaultPageSize, offset: this.defaultOffset, data: { data: [], totalCount: 0 } },
      "In Progress": { search: this.defaultSearch, pagesize: this.defaultPageSize, offset: this.defaultOffset, data: { data: [], totalCount: 0 } },
      "Completed": { search: this.defaultSearch, pagesize: this.defaultPageSize, offset: this.defaultOffset, data: { data: [], totalCount: 0 } }
    }

  constructor(private router: Router, jobService: JobService) {
    this.jobService = jobService
  }

  ngOnInit(): void {
    this.loadDataToTable(this.defaultSearch, this.defaultPageSize, this.defaultOffset);
  }

  onTabChange(event: MatTabChangeEvent) {
    this.selectedTab = (event.tab.textLabel as "Created" | "In Progress" | "Completed");
    this.loadDataToTable(this.tabStates[this.selectedTab].search, this.tabStates[this.selectedTab].pagesize, this.tabStates[this.selectedTab].offset)
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    const tabToApiMap: Record<typeof this.selectedTab, string> = {
      "Created": "created",
      "In Progress": "in-progress",
      "Completed": "completed"
    };

    const statusQuery: "created" | "in-progress" | "completed" = tabToApiMap[this.selectedTab] as "created" | "in-progress" | "completed";;
    this.jobService.getJob(statusQuery, { search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        switch (this.selectedTab) {
          case "Created":
            this.tabStates["Created"].data = response
            this.tabStates["Created"].pagesize = pageSize
            this.tabStates["Created"].offset = offSet
            this.tabStates["Created"].search = searchTerm
            break;
          case "In Progress":
            this.tabStates["In Progress"].data = response
            this.tabStates["In Progress"].pagesize = pageSize
            this.tabStates["In Progress"].offset = offSet
            this.tabStates["In Progress"].search = searchTerm
            break;
          case "Completed":
            this.tabStates["Completed"].data = response
            this.tabStates["Completed"].pagesize = pageSize
            this.tabStates["Completed"].offset = offSet
            this.tabStates["Completed"].search = searchTerm
            break;
          default:
            throw new Error("Got a non-valid tab option when fetching")
        }
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
