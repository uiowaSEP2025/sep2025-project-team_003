import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import { MatButtonModule } from '@angular/material/button';
import { DiscountsService } from '../../../services/discount.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-discounts-page',
  imports: [MatInputModule, ReactiveFormsModule, MatButtonModule],
  templateUrl: './create-discounts-page.component.html',
  styleUrl: './create-discounts-page.component.scss'
})
export class CreateDiscountsPageComponent {
  private numberPattern = /^(100(?:\.0{1,2})?|[0-9]{1,2}(?:\.\d{1,2})?)$/;
  nameControl = new FormControl('', [Validators.required])
  percentControl = new FormControl('', [Validators.required, Validators.pattern(this.numberPattern), Validators.min(0), Validators.max(100)])
  matcher = new GenericFormErrorStateMatcher()

  constructor(private discountService: DiscountsService, private router:Router) {

  }

  onSubmit() {
    if (this.nameControl.invalid || this.percentControl.invalid) {
      return
    }

    const formdata = {
      name: this.nameControl.value,
      percent: this.percentControl.value
    }
    this.discountService.createDiscount(formdata).subscribe({
      next: (response) => {
        this.router.navigate(['/discounts']);
      },
      error: (error) => {
      }
    }
    )
  }

}
