import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { ServiceService } from '../../services/service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-jobs-page',
  imports: [TableComponentComponent],
  templateUrl: './create-jobs-page.component.html',
  styleUrl: './create-jobs-page.component.scss'
})
export class CreateJobsPageComponent implements OnInit {
  serviceService: ServiceService
  services: any
  checkedServices: number[]

  constructor(private router: Router, serviceService: ServiceService) {
    this.checkedServices = []
    this.serviceService = serviceService
  }


  setCheckedServices(ids: number[]) {
    this.checkedServices = [...ids] // in order for change
  }

  loadServiceToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.serviceService.getService({ search: searchTerm, pagesize: pageSize, offset: offSet }).subscribe({
      next: (response) => {
        this.services = response
      },
      error: (error) => {
        if (error.status === 401) {
          this.router.navigate(['/login']);
        }
      }
    })
  }

  ngOnInit(): void {
    this.loadServiceToTable("", 5, 0);
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }

}
