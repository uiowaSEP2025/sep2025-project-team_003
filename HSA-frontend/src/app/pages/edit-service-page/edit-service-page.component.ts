import { Component } from '@angular/core';
import {MatButton} from "@angular/material/button";
import {MatError, MatFormField, MatLabel} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-edit-service-page',
    imports: [
        MatButton,
        MatError,
        MatFormField,
        MatInput,
        MatLabel,
        ReactiveFormsModule
    ],
  templateUrl: './edit-service-page.component.html',
  styleUrl: './edit-service-page.component.scss'
})
export class EditServicePageComponent {
  serviceForm: FormGroup;

  constructor(private router: Router, private activatedRoute: ActivatedRoute, private serviceFormBuilder: FormBuilder) {
    this.serviceForm = this.serviceFormBuilder.group({
      serviceName: ['', Validators.required],
      serviceDescription: ['', Validators.required],
    });

    this.activatedRoute.queryParams.subscribe(params => {
      this.serviceForm.controls['serviceName'].setValue(params['fname']);
      this.serviceForm.controls['serviceDescription'].setValue(params['lname']);
    })
  }

  onSubmit() {
    if (this.serviceForm.invalid) {
      this.serviceForm.markAllAsTouched();
      return;
    } else {
      console.log("Submitted");
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
