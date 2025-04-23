import { Component, ViewChild } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { MatTab, MatTabChangeEvent, MatTabsModule } from '@angular/material/tabs';
import { Router } from '@angular/router';
import { RequestService } from '../../services/request.service';
import { MatDialog } from '@angular/material/dialog';
import { ViewRequestComponentComponent } from '../../components/view-request-component/view-request-component.component';

@Component({
  selector: 'app-request-dashboard-page',
  imports: [
    TableComponentComponent, 
    MatButtonModule, 
    MatIconModule, 
    LoadingFallbackComponent, 
    CommonModule, 
    MatTabsModule
  ],
  templateUrl: './request-dashboard-page.component.html',
  styleUrl: './request-dashboard-page.component.scss'
})
export class RequestDashboardPageComponent {
  approvedRequests: any
  pendingRequests: any
  currentTabLabel: string = 'approved';

  constructor(
    private router: Router, 
    public requestService: RequestService,
    private dialog: MatDialog
  ) {
  }

  ngOnInit(): void {
    this.loadApprovedDataToTable("", 5, 0, "approved");
    this.loadPendingDataToTable("", 5, 0, "received")
  }

  loadApprovedDataToTable(searchTerm: string, pageSize: number, offSet: number, status?: string) {
    this.requestService.getFilteredRequest({ status: status, search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.approvedRequests = response
      },
      error: (error) => {
      }
    })
  }

  loadPendingDataToTable(searchTerm: string, pageSize: number, offSet: number, status?: string) {
    this.requestService.getFilteredRequest({ status: status,  search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.pendingRequests = response
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
    this.currentTabLabel = event.tab.textLabel.toLowerCase();
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
