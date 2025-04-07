import { Component } from '@angular/core';
import {ReactiveFormsModule} from '@angular/forms';
import {MaterialsHelperComponent} from '../materials-helper/materials-helper.component';

@Component({
  selector: 'app-create-material-page',
  imports: [
    ReactiveFormsModule,
    MaterialsHelperComponent
  ],
  templateUrl: './create-material-page.component.html',
  styleUrl: './create-material-page.component.scss'
})
export class CreateMaterialPageComponent {

}
