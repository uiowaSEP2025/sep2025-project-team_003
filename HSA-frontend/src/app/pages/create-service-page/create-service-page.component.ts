import { Component } from '@angular/core';
import {MatButton} from '@angular/material/button';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {Router} from '@angular/router';

@Component({
  selector: 'app-create-service-page',
  imports: [
    MatButton,
    MatError,
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule
  ],
  templateUrl: './create-service-page.component.html',
  styleUrl: './create-service-page.component.scss'
})
export class CreateServicePageComponent {
  serviceForm: FormGroup;

  constructor(private router: Router, private serviceFormBuilder: FormBuilder) {
    this.serviceForm = this.serviceFormBuilder.group({
      serviceName: ['', Validators.required],
      serviceDescription: [''],
    });
  }

  onSubmit() {
    if (this.serviceForm.invalid) {
      this.serviceForm.markAllAsTouched();
      return;
    } else {
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
