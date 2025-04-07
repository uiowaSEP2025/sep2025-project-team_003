import {Component, Input} from '@angular/core';
import {ReactiveFormsModule} from '@angular/forms';
import {MaterialsHelperComponent} from '../materials-helper/materials-helper.component';
import {Material} from '../../../interfaces/material.interface';

@Component({
  selector: 'app-edit-material-page',
  imports: [
    ReactiveFormsModule,
    MaterialsHelperComponent
  ],
  templateUrl: './edit-material-page.component.html',
  styleUrl: './edit-material-page.component.scss'
})
export class EditMaterialPageComponent {
  @Input()  material: Material = {
    organizationID: 0,
    materialID: 0,
    materialName: '',
    materialDescription: '',
    defaultCost: 0
  }
}
