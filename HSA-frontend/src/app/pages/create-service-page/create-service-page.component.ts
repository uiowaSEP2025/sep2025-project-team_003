import { Component } from '@angular/core';
import {MatButton} from '@angular/material/button';
import {MatError, MatFormField, MatLabel} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import { ServiceService } from '../../services/service.service';
import { MatSnackBar } from '@angular/material/snack-bar';

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

  constructor(private router: Router, private serviceFormBuilder: FormBuilder, private serviceService: ServiceService, private snackBar: MatSnackBar) {
    this.serviceForm = this.serviceFormBuilder.group({
      serviceName: ['', Validators.required],
      serviceDescription: [''],
      serviceDefaultFee: [''],
    });
  }

  onSubmit() {
    if (this.serviceForm.invalid) {
      this.serviceForm.markAllAsTouched();
      return;
    } else {
      const data = {
        service_name: this.serviceForm.controls["serviceName"].value,
        service_description: this.serviceForm.controls["serviceDescription"].value,
        default_fee: this.serviceForm.controls["serviceDefaultFee"].value,
      }
      this.serviceService.createService(data).subscribe({
        next: () => {
          this.snackBar.open('Created service successfully', '', {
            duration: 3000
          });
          this.navigateToPage('services');
        },
        error: (error) => {
        }
      });
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
