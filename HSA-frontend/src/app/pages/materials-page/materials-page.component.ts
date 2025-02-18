import { Component } from '@angular/core';
import {Router} from '@angular/router';
import {MatFabButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {TableComponentComponent} from '../../components/table-component/table-component.component';

@Component({
  selector: 'app-materials-page',
  imports: [
    MatFabButton,
    MatIcon,
    TableComponentComponent
  ],
  templateUrl: './materials-page.component.html',
  styleUrl: './materials-page.component.scss'
})
export class MaterialsPageComponent {
  constructor(private router: Router) {}

  redirectCreate() {
    this.router.navigate(['/materials/create']);
  }
}
