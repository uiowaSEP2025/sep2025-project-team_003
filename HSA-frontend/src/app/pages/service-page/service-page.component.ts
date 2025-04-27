import { Component, OnInit } from '@angular/core';
import {MatFabButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {TableComponentComponent} from '../../components/table-component/table-component.component';
import {Router} from '@angular/router';
import { ServiceService } from '../../services/service.service';
import { CommonModule } from '@angular/common';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';

@Component({
  selector: 'app-service-page',
  imports: [
    TableComponentComponent,
    MatFabButton,
    MatIcon,
    CommonModule,
    LoadingFallbackComponent
  ],
  templateUrl: './service-page.component.html',
  styleUrl: './service-page.component.scss'
})
export class ServicePageComponent implements OnInit {
  services: any = null;
  serviceService: ServiceService
  
  constructor(private router: Router, serviceService: ServiceService) {
    this.serviceService = serviceService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.serviceService.getService({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.services = response
      },
      error: (error) => {
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
