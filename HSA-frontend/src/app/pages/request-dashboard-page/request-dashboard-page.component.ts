import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import {  MatTabChangeEvent, MatTabsModule } from '@angular/material/tabs';
import { Router } from '@angular/router';
import { RequestService } from '../../services/request.service';
import { MatDialog } from '@angular/material/dialog';
import { ViewRequestComponentComponent } from '../../components/view-request-component/view-request-component.component';
import { TableApiResponse } from '../../interfaces/api-responses/table.api.interface';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';

@Component({
  selector: 'app-request-dashboard-page',
  imports: [
    TableComponentComponent,
    MatButtonModule,
    MatIconModule,
    LoadingFallbackComponent,
    CommonModule,
    MatTabsModule,
    PageTemplateComponent,
  ],
  templateUrl: './request-dashboard-page.component.html',
  styleUrl: './request-dashboard-page.component.scss'
})
export class RequestDashboardPageComponent {
  tabStates: Record<'Approved' | 'Pending', {
    search: string;
    pagesize: number;
    offset: number;
    data: TableApiResponse<any>;
  }> = {
    Approved: { search: '', pagesize: 5, offset: 0, data: {data: [], totalCount: 0} },
    Pending: { search: '', pagesize: 5, offset: 0, data: {data: [], totalCount: 0} }
  };
  currentTabLabel: "Approved" | "Pending" = 'Approved';

  constructor(
    private router: Router,
    public requestService: RequestService,
    private dialog: MatDialog
  ) {
  }

  hasNoData = () => ((this.currentTabLabel === "Pending" && this.tabStates.Pending.data === null) || (this.currentTabLabel === "Approved" && this.tabStates.Approved.data === null))

  ngOnInit(): void {
    this.loadDataToTable(this.tabStates.Approved.search, this.tabStates.Approved.pagesize, this.tabStates.Approved.offset);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    const tabToApiMap: Record<typeof this.currentTabLabel, string> = {
      "Approved": "approved",
      "Pending": "received"
    };

    const statusQuery = tabToApiMap[this.currentTabLabel]
    this.requestService.getFilteredRequest({ status: statusQuery, search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        switch (this.currentTabLabel) {
          case "Approved":
            this.tabStates["Approved"].data = response
            this.tabStates["Approved"].pagesize = pageSize
            this.tabStates["Approved"].offset = offSet
            this.tabStates["Approved"].search = searchTerm
            break;
          case "Pending":
            this.tabStates["Pending"].data = response
            this.tabStates["Pending"].pagesize = pageSize
            this.tabStates["Pending"].offset = offSet
            this.tabStates["Pending"].search = searchTerm
            break;
          default:
            throw new Error("Got a non-valid tab option when fetching")
        }
      },
      error: (error) => {
      }
    })

  }

  redirectRequestDetails(element: any) {
    const dialogRef = this.dialog.open(ViewRequestComponentComponent, {
      width: 'auto',
      maxWidth: '90vw',
      height: 'auto',
      data: {
        info: element,
        status: this.currentTabLabel
      }
    });
  }

  onTabChange(event: MatTabChangeEvent) {
    this.currentTabLabel = event.tab.textLabel as "Approved" | "Pending";
    this.loadDataToTable(this.tabStates[this.currentTabLabel].search, this.tabStates[this.currentTabLabel].pagesize, this.tabStates.Approved.offset);
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
