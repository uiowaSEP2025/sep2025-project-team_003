import {Component} from '@angular/core';
import { ReactiveFormsModule,FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import {ContractorsHelperComponent} from '../contractors-helper/contractors-helper.component';

@Component({
  selector: 'app-create-contractors-page',
  imports: [MatInputModule, ReactiveFormsModule, FormsModule, ContractorsHelperComponent],
  templateUrl: './create-contractor-page.component.html',
  styleUrl: './create-contractor-page.component.scss'
})
export class CreateContractorPageComponent {

}
