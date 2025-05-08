import { Component, OnInit } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatError } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { OrganizationService } from '../../services/organization.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';

@Component({
  selector: 'app-update-payment-page',
  imports: [
    MatInputModule,
    MatError,
    MatButtonModule,
    MatCardModule,
    CommonModule,
    ReactiveFormsModule,
    PageTemplateComponent
  ],
  templateUrl: './update-payment-page.component.html',
  styleUrl: './update-payment-page.component.scss'
})
export class UpdatePaymentPageComponent implements OnInit {
  url = new FormControl("", [Validators.required,
    Validators.pattern(/^https?:\/\/((([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}|localhost|\d{1,3}(\.\d{1,3}){3}))(:\d+)?(\/[^\s?#]*)?(\?[^\s#]*)?(#[^\s]*)?$/)
  ])

    constructor (private router: Router,
      private orgservice:OrganizationService,
      private snackbar: MatSnackBar
    ) {}

  ngOnInit(): void {
    this.orgservice.getPayemntLink().subscribe(
      {
        next: (resp) => {
          this.url.setValue(resp.URL)
        },
        error: () => {}
      }
    )
  }

  backHome() {this.router.navigate(['/'])}

  update() {
    this.url.markAsTouched()
    if (!this.url.valid) {return}
    this.orgservice.setPayemntLink({url: this.url.value}).subscribe({
      next: () => {
        this.router.navigate(['/'])
        this.snackbar.open('Payment link set!', '', {
          duration: 3000
        });


      }
    })

  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
