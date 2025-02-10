import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';

@Component({
  selector: 'app-test-page',
  imports: [TableComponentComponent],
  templateUrl: './test-page.component.html',
  styleUrl: './test-page.component.scss'
})
export class TestPageComponent {

}
