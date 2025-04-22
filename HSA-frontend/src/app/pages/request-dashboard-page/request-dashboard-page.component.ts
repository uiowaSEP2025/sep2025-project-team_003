import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { RequestService } from '../../services/request.service';

@Component({
  selector: 'app-request-dashboard-page',
  imports: [TableComponentComponent, MatButtonModule, MatIconModule, LoadingFallbackComponent, CommonModule],
  templateUrl: './request-dashboard-page.component.html',
  styleUrl: './request-dashboard-page.component.scss'
})
export class RequestDashboardPageComponent {
  requests: any

  constructor(private router: Router, public requestService: RequestService) {
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.requestService.getRequest({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.requests = response
      },
      error: (error) => {
      }
    })
  }

  redirectRequestDetails(element: any) {
    this.router.navigate([`/request/${element.id}`])
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
