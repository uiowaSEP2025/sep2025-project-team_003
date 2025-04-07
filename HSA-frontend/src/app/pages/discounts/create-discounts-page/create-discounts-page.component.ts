import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import { MatButtonModule } from '@angular/material/button';
import { DiscountsService } from '../../../services/discount.service';
import { Router } from '@angular/router';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import {DiscountsHelperComponent} from '../discounts-helper/discounts-helper.component';

@Component({
  selector: 'app-create-discounts-page',
  imports: [MatInputModule, ReactiveFormsModule, MatButtonModule, DiscountsHelperComponent],
  templateUrl: './create-discounts-page.component.html',
  styleUrl: './create-discounts-page.component.scss'
})
export class CreateDiscountsPageComponent {

}
