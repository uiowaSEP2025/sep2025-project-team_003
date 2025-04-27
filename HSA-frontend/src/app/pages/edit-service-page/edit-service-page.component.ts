import { Component } from '@angular/core';
import {MatButton} from "@angular/material/button";
import {MatError, MatFormField, MatLabel} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {ActivatedRoute, Router} from '@angular/router';
import { ServiceService } from '../../services/service.service';

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
  public currentServiceName: string;
  serviceID: number | null = null

  constructor(private router: Router, private activatedRoute: ActivatedRoute, private serviceFormBuilder: FormBuilder, private serviceService: ServiceService) {
    this.serviceForm = this.serviceFormBuilder.group({
      serviceName: ['', Validators.required],
      serviceDescription: [''],
    });

    this.activatedRoute.queryParams.subscribe(params => {
      this.serviceForm.controls['serviceName'].setValue(params['service_name']);
      this.serviceForm.controls['serviceDescription'].setValue(params['service_description']);
    })

    this.activatedRoute.paramMap.subscribe(params => {
      this.serviceID = Number(params.get('id'));
    })

    this.currentServiceName = this.serviceForm.controls['serviceName'].value
  }

  onSubmit() {
    if (this.serviceForm.invalid) {
      this.serviceForm.markAllAsTouched();
      return;}
      const data = {
        id: this.serviceID,
        service_name: this.serviceForm.controls['serviceName'].value,
        service_description: this.serviceForm.controls['serviceDescription'].value
      }
      this.serviceService.editService(data).subscribe(
        {next: (response) => {
          this.router.navigate(['/services']);
        },
        error: (error) => {
        }}
      )
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
