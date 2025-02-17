import { Component } from '@angular/core';
import { GenericFormErrorStateMatcher } from '../../utils/generic-form-error-state-matcher';
import { FormControl,ReactiveFormsModule,FormsModule, Validators } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButton } from '@angular/material/button';

@Component({
  selector: 'app-create-contractors-page',
  imports: [MatInputModule,ReactiveFormsModule,FormsModule, MatButton],
  templateUrl: './create-contractors-page.component.html',
  styleUrl: './create-contractors-page.component.scss'
})
export class CreateContractorsPageComponent {

    firstNameControl = new FormControl('', Validators.required)
    lastNameControl = new FormControl('', Validators.required)
    emailControl = new FormControl('', [Validators.email, Validators.required])
    phoneControl = new FormControl('', Validators.required)
    matcher = new GenericFormErrorStateMatcher()

}
