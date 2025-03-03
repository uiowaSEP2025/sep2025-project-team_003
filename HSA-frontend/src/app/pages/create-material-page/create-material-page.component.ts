import { Component } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {MatButton} from '@angular/material/button';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import { MaterialService } from '../../services/material.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-material-page',
  imports: [
    MatButton,
    MatError,
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule
  ],
  templateUrl: './create-material-page.component.html',
  styleUrl: './create-material-page.component.scss'
})
export class CreateMaterialPageComponent {
  materialForm: FormGroup;

  constructor(private router: Router, private materialFormBuilder: FormBuilder, private materialService: MaterialService , private snackBar: MatSnackBar) {
    this.materialForm = this.materialFormBuilder.group({
      materialName: ['', Validators.required],
      materialDescription: [''],
    });
  }

  onSubmit() {
    if (this.materialForm.invalid) {
      this.materialForm.markAllAsTouched();
      return;
    } else {
      this.materialService.createMaterial({
        material_name: this.materialForm.controls["materialName"].value
      }).subscribe({
        next: () => {
          this.snackBar.open('Create material successfully', '', {
            duration: 3000
          });
          this.navigateToPage('materials');
        },
        error: (error) => {
          if (error.status === 401) {
            if (error.status === 401) {
              this.router.navigate(['/login']);
            }
          }
        }
      });
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
