import {Component, Input} from '@angular/core';
import {ReactiveFormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatButtonModule} from '@angular/material/button';
import {Discount} from '../../../interfaces/discount.interface';
import {DiscountsHelperComponent} from '../discounts-helper/discounts-helper.component';

@Component({
  selector: 'app-edit-discount-page',
  imports: [MatInputModule, MatButtonModule, ReactiveFormsModule, DiscountsHelperComponent],
  templateUrl: './edit-discount-page.component.html',
  styleUrl: './edit-discount-page.component.scss'
})
export class EditDiscountPageComponent {
  @Input() discount: Discount = {
    discountID: 0, discountName: "", discountPercent: 0,

  };

}
