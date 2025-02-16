import { Component } from '@angular/core';
import { environment } from '../../../environments/environment'

@Component({
  selector: 'app-test-page',
  imports: [],
  templateUrl: './test-page.component.html',
  styleUrl: './test-page.component.scss'
})
export class TestPageComponent {
  url = environment.apiUrl
}
