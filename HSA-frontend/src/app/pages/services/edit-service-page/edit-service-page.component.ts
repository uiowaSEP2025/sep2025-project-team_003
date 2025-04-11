import {Component, Input} from '@angular/core';
import {ReactiveFormsModule} from "@angular/forms";
import {ServicesHelperComponent} from '../services-helper/services-helper.component';
import {Service} from '../../../interfaces/service.interface';

@Component({
  selector: 'app-edit-service-page',
  imports: [
    ReactiveFormsModule,
    ServicesHelperComponent
  ],
  templateUrl: './edit-service-page.component.html',
  styleUrl: './edit-service-page.component.scss'
})
export class EditServicePageComponent {
  @Input() service: Service = {
    organizationID: 0,
    serviceID: 0,
    serviceName: '',
    serviceDescription: '',
    defaultRate: 0,
  }

}
