import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';


@Component({
  selector: 'app-customers-page',
  imports: [TableComponentComponent, MatButtonModule, MatIconModule],
  templateUrl: './customers-page.component.html',
  styleUrl: './customers-page.component.scss'
})
export class CustomersPageComponent {
  constructor(private router: Router) {}

  redirectCreate() {
    this.router.navigate(['/customers/create'],{
      
    });
  }

}
