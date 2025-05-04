import { Component, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { GenericFormErrorStateMatcher } from '../../../utils/generic-form-error-state-matcher';
import { MatButtonModule } from '@angular/material/button';
import { DiscountsService } from '../../../services/discount.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-edit-discount-page',
  imports: [MatInputModule, MatButtonModule, ReactiveFormsModule],
  templateUrl: './edit-discount-page.component.html',
  styleUrl: './edit-discount-page.component.scss'
})
export class EditDiscountPageComponent implements OnInit{
  private numberPattern = /^(100(?:\.0{1,2})?|[0-9]{1,2}(?:\.\d{1,2})?)$/;
  nameControl = new FormControl('', [Validators.required])
  percentControl = new FormControl('', [Validators.required, Validators.pattern(this.numberPattern), Validators.min(0), Validators.max(100)])
  matcher = new GenericFormErrorStateMatcher()
  name!: string
  percent!: string
  id!: string | null


  constructor(private discountService: DiscountsService, private router:Router, private activatedRoute: ActivatedRoute) {

  }

  private parsePercentage(input: string): string {
    const cleaned = input.replace('%', '').trim();
    return cleaned;
  }

  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      this.name = params["discount_name"]

      this.percent = params['discount_percent'];
      this.nameControl.setValue(this.name);
      this.percentControl.setValue(this.parsePercentage(this.percent));

    });

    this.activatedRoute.paramMap.subscribe(params => {
      this.id = params.get('id');
    })
  }

  onSubmit() {
    if (this.nameControl.invalid || this.percentControl.invalid) {
      return
    }

    const formdata = {
      name: this.nameControl.value,
      percent: this.percentControl.value,
      id: this.id
    }

    this.discountService.editDiscount(formdata).subscribe({
      next: (response) => {
        this.router.navigate(['/discounts']);
      },
      error: (error) => {
      }
    }
    )
  }
}
