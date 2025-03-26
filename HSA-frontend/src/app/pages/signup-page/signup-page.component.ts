import {ChangeDetectionStrategy, Component, OnInit} from '@angular/core';
import { Router } from '@angular/router';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatButton} from '@angular/material/button';
import {MatOption, MatSelect} from '@angular/material/select';
import {HttpClient} from '@angular/common/http';

interface State {
  name: string,
  code: string
}

@Component({
  selector: 'app-signup-page',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatButton,
    MatSelect,
    MatOption
  ],
  templateUrl: './signup-page.component.html',
  styleUrl: './signup-page.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})

export class SignupPageComponent implements OnInit {
  registrationForm: FormGroup;
  states: State[] = [
      { "name":  "Alabama", "code":  "AL"},
      { "name":  "Alaska", "code":  "AK"},
      { "name":  "Arkansas", "code":  "AR"},
      { "name":  "California", "code":  "CA"},
      { "name":  "Colorado", "code":  "CO"},
      { "name":  "Connecticut", "code":  "CT"},
      { "name":  "Delaware", "code":  "DE"},
      { "name":  "District of Columbia", "code":  "DC"},
      { "name":  "Florida", "code":  "FL"},
      { "name":  "Georgia", "code":  "GA"},
      { "name":  "Hawaii", "code":  "HI"},
      { "name":  "Idaho", "code":  "ID"},
      { "name":  "Illinois", "code":  "IL"},
      { "name":  "Indiana", "code":  "IN"},
      { "name":  "Iowa", "code":  "IA"},
      { "name":  "Kansas", "code":  "KS"},
      { "name":  "Kentucky", "code":  "KY"},
      { "name":  "Louisiana", "code":  "LA"},
      { "name":  "Maine", "code":  "ME"},
      { "name":  "Maryland", "code":  "MD"},
      { "name":  "Massachusetts", "code":  "MA"},
      { "name":  "Michigan", "code":  "MI"},
      { "name":  "Minnesota", "code":  "MN"},
      { "name":  "Mississippi", "code":  "MS"},
      { "name":  "Missouri", "code":  "MO"},
      { "name":  "Montana", "code":  "MT"},
      { "name":  "Nebraska", "code":  "NE"},
      { "name":  "Nevada", "code":  "NV"},
      { "name":  "New Hampshire", "code":  "NH"},
      { "name":  "New Jersey", "code":  "NJ"},
      { "name":  "New Mexico", "code":  "NM"},
      { "name":  "New York", "code":  "NY"},
      { "name":  "North Carolina", "code":  "NC"},
      { "name":  "North Dakota", "code":  "ND"},
      { "name":  "Ohio", "code":  "OH"},
      { "name":  "Oklahoma", "code":  "OK"},
      { "name":  "Oregon", "code":  "OR"},
      { "name":  "Pennsylvania", "code":  "PA"},
      { "name":  "Rhode Island", "code":  "RI"},
      { "name":  "South Carolina", "code":  "SC"},
      { "name":  "South Dakota", "code":  "SD"},
      { "name":  "Tennessee", "code":  "TN"},
      { "name":  "Texas", "code":  "TX"},
      { "name":  "Utah", "code":  "UT"},
      { "name":  "Vermont", "code":  "VT"},
      { "name":  "Virginia", "code":  "VA"},
      { "name":  "Washington", "code":  "WA"},
      { "name":  "West Virginia", "code":  "WV"},
      { "name":  "Wisconsin", "code":  "WI"},
      { "name":  "Wyoming", "code":  "WY"}
    ]

  constructor(private router: Router, private registrationFormBuilder: FormBuilder, private http: HttpClient) {
    this.registrationForm = this.registrationFormBuilder.group({
      organizationName: ['', Validators.required],
      organizationEmail: ['', [Validators.required, Validators.email]],
      addressOne: ['', Validators.required],
      ownerName: ['', Validators.required],
      stateSelect: ['', Validators.required],
    });
  }

  ngOnInit() {
  }

  onSubmit() {
    if (this.registrationForm.invalid) {
      this.registrationForm.markAllAsTouched();
      return;
    } else {
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
