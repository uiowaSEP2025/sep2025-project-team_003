import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';

@Component({
  selector: 'app-customers-page',
  imports: [TableComponentComponent],
  templateUrl: './customers-page.component.html',
  styleUrl: './customers-page.component.scss'
})
export class CustomersPageComponent {

}
