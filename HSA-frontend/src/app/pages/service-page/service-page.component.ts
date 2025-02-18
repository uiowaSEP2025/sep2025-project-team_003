import { Component } from '@angular/core';
import {MatFabButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {TableComponentComponent} from '../../components/table-component/table-component.component';
import {Router} from '@angular/router';

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
  constructor(private router: Router) {}

  redirectCreate() {
    this.router.navigate(['/services/create']);
  }

}
