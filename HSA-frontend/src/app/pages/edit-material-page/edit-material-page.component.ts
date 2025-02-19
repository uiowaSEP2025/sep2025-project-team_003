import { Component } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {MatButton} from '@angular/material/button';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';

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
export class EditMaterialPageComponent {
  materialForm: FormGroup;
  public currentMaterialName: string;

  constructor(private router: Router, private activatedRoute: ActivatedRoute, private materialFormBuilder: FormBuilder) {
    this.materialForm = this.materialFormBuilder.group({
      materialName: ['', Validators.required],
      materialDescription: [''],
    });

    this.activatedRoute.queryParams.subscribe(params => {
      this.materialForm.controls['materialName'].setValue(params['fname']);
      this.materialForm.controls['materialDescription'].setValue(params['lname']);
    })

    this.currentMaterialName = this.materialForm.controls['materialName'].value
  }

  onSubmit() {
    if (this.materialForm.invalid) {
      this.materialForm.markAllAsTouched();
      return;
    } else {
      console.log("Submitted");
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
