import {ChangeDetectionStrategy, Component, Injectable, OnInit} from '@angular/core';
import { Router } from '@angular/router';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatButton} from '@angular/material/button';
import {MatOption, MatSelect} from '@angular/material/select';
import {HttpClient} from '@angular/common/http';


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

@Injectable({providedIn: 'root'})
export class SignupPageComponent implements OnInit {
  registrationForm: FormGroup;
  states: any[] = [];

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
    this.loadStates();
  }

  loadStates() {
    this.http.get<any[]>('states.json').subscribe(
      (data: any[]) => {
        this.states = data;
      }
    )
  }

  onSubmit() {
    if (this.registrationForm.invalid) {
      this.registrationForm.markAllAsTouched();
      return;
    } else {
      console.log("Submitted");
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
