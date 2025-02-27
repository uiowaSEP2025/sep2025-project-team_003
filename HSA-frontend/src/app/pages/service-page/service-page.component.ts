import { Component } from '@angular/core';
import {MatFabButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {TableComponentComponent} from '../../components/table-component/table-component.component';
import {Router} from '@angular/router';
import { ServiceService } from '../../services/service.service';

@Component({
  selector: 'app-service-page',
  imports: [
    TableComponentComponent,
    MatFabButton,
    MatIcon
  ],
  templateUrl: './service-page.component.html',
  styleUrl: './service-page.component.scss'
})
export class ServicePageComponent {
  serviceService: ServiceService
  
  constructor(private router: Router, serviceService: ServiceService) {
    this.serviceService = serviceService
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
