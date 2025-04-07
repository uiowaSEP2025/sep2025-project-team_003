import {Component, Input, OnInit} from '@angular/core';
import {
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatInput, MatLabel} from '@angular/material/input';
import {FormControl, ReactiveFormsModule, Validators} from '@angular/forms';
import {MatError, MatFormField} from '@angular/material/form-field';
import {MatButton} from '@angular/material/button';
import {Router} from '@angular/router';
import {MaterialService} from '../../../services/material.service';
import {ErrorHandlerService} from '../../../services/error.handler.service';
import {Material} from '../../../interfaces/material.interface';
import {GenericFormErrorStateMatcher} from '../../../utils/generic-form-error-state-matcher';
import {CreateMaterialPageComponent} from '../create-material-page/create-material-page.component';

@Component({
  selector: 'app-materials-helper',
  imports: [
    MatDialogActions,
    MatDialogClose,
    MatDialogTitle,
    MatError,
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule,
    MatButton,
    MatDialogContent
  ],
  templateUrl: './materials-helper.component.html',
  styleUrl: './materials-helper.component.scss'
})
export class MaterialsHelperComponent implements OnInit {
  @Input() crudType: 'Create' | 'Update' = 'Create';
  @Input() material: Material = {
    defaultCost: 0, materialDescription: '', materialID: 0, materialName: '', organizationID: 0

  }
  nameControl = new FormControl('', Validators.required)
  descriptionControl = new FormControl('')
  defaultCostControl = new FormControl(0)
  matcher = new GenericFormErrorStateMatcher()

  private isFormValid() {
    return this.nameControl.valid;
  }

  constructor(public dialogRef: MatDialogRef<CreateMaterialPageComponent>, private materialService: MaterialService, private router: Router, private errorHandler: ErrorHandlerService) {
  }

  ngOnInit() {
    if (this.crudType === 'Update') {
      this.nameControl = new FormControl(this.material.materialName, Validators.required)
      this.descriptionControl = new FormControl(this.material.materialDescription)
      this.defaultCostControl = new FormControl(this.material.defaultCost)
    }
  }

  onSubmit() {
    if (!this.isFormValid()) {
      return
    }
    const args = {
      id: 0,
      material_name: this.nameControl.value,
      material_description: this.descriptionControl.value,
      default_cost: this.defaultCostControl.value
    }
    if(!args.default_cost) {
      args.default_cost = 0
    }
    if (this.crudType === 'Update') {
      args.id = this.material.materialID
      this.materialService.editMaterial(args).subscribe(
        {
          next: () => {
            this.dialogRef.close();
            window.location.reload();
          },
          error: (error) => {
            this.errorHandler.handleError(error);
          }
        }
      )
    }
    else {
      this.materialService.createMaterial(args).subscribe({
        next: () => {
          this.dialogRef.close();
          window.location.reload();
        },
        error: (error) => {
          this.errorHandler.handleError(error);
        }
        }
      )
    }
  }

}
