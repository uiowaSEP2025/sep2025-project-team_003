import { Component } from '@angular/core';
import {ReactiveFormsModule} from '@angular/forms';
import {ServicesHelperComponent} from '../services-helper/services-helper.component';

@Component({
  selector: 'app-create-service-page',
  imports: [
    ReactiveFormsModule,
    ServicesHelperComponent
  ],
  templateUrl: './create-service-page.component.html',
  styleUrl: './create-service-page.component.scss'
})
export class CreateServicePageComponent {

}
