import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import { Router } from '@angular/router';

@Component({
  selector: 'app-contractors-page',
  imports: [TableComponentComponent, MatButtonModule, MatIcon],
  templateUrl: './contractors-page.component.html',
  styleUrl: './contractors-page.component.scss'
})
export class ContractorsPageComponent {
  constructor(private router: Router) {}

  redirectCreate() {
    this.router.navigate(['/contractors/create']);
  }

}
