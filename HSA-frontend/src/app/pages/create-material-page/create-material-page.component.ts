import { Component } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {MatButton} from '@angular/material/button';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';

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

  constructor(private router: Router, private materialFormBuilder: FormBuilder) {
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
      console.log("Submitted");
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
