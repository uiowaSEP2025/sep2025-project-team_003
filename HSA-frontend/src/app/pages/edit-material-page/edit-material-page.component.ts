import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {MatButton} from '@angular/material/button';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import { MaterialService } from '../../services/material.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-edit-material-page',
  imports: [
    MatButton,
    MatError,
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule
  ],
  templateUrl: './edit-material-page.component.html',
  styleUrl: './edit-material-page.component.scss'
})
export class EditMaterialPageComponent implements OnInit {
  materialForm: FormGroup;
  public currentMaterialName: string;
  private materialID: number | null = null;

  constructor(private router: Router, private activatedRoute: ActivatedRoute, private materialFormBuilder: FormBuilder, private materialService: MaterialService, private snackBar: MatSnackBar) {
    this.materialForm = this.materialFormBuilder.group({
      materialName: ['', Validators.required],
      materialDescription: [''],
    });

    this.activatedRoute.queryParams.subscribe(params => {
      this.materialForm.controls['materialName'].setValue(params['material_name']);
    })

    this.currentMaterialName = this.materialForm.controls['materialName'].value;
  }

  ngOnInit() {
    this.activatedRoute.paramMap.subscribe(params => {
      this.materialID = Number(params.get('id'));
    })
  }

  onSubmit() {
    if (this.materialForm.invalid) {
      this.materialForm.markAllAsTouched();
      return;
    } else {
      this.materialService.editMaterial({
        material_name: this.materialForm.controls["materialName"].value,
        id: this.materialID
      }).subscribe({
        next: () => {
          this.snackBar.open(`Edit ${this.currentMaterialName} material to ${this.materialForm.controls["materialName"].value} successfully`, '', {
            duration: 3000
          });
          this.navigateToPage('materials')
        },
        error: (error) => {
          if (error.status === 401) {
            this.router.navigate(['/login']);
          }
        }
      });
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
