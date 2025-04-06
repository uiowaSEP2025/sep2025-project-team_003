import {Component, Input} from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import {ContractorsHelperComponent} from "../contractors-helper/contractors-helper.component";
import {Contractor} from "../../../interfaces/contractor.interface";

@Component({
  selector: 'app-edit-contractors-page',
  imports: [
    MatFormFieldModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    FormsModule,
    ContractorsHelperComponent
  ],
  templateUrl: './edit-contractors-page.component.html',
  styleUrl: './edit-contractors-page.component.scss'
})
export class EditContractorsPageComponent {
  @Input() contractor: Contractor = {
    organizationID: 0,
    contractorID: 0,
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
  };
}
