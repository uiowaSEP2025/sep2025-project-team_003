import {Component, Input, OnInit} from '@angular/core';
import {FormControl, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatError, MatFormField, MatInput, MatLabel} from "@angular/material/input";
import {GenericFormErrorStateMatcher} from '../../../utils/generic-form-error-state-matcher';
import {DiscountsService} from '../../../services/discount.service';
import {ActivatedRoute} from '@angular/router';
import {ErrorHandlerService} from '../../../services/error.handler.service';
import {MatButton} from '@angular/material/button';
import {CreateDiscountsPageComponent} from '../create-discounts-page/create-discounts-page.component';
import {Discount} from '../../../interfaces/discount.interface';

@Component({
  selector: 'app-discounts-helper',
  imports: [
    FormsModule,
    MatButton,
    MatDialogActions,
    MatDialogClose,
    MatDialogContent,
    MatDialogTitle,
    MatError,
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule,
    MatError,
    MatFormField
  ],
  templateUrl: './discounts-helper.component.html',
  styleUrl: './discounts-helper.component.scss'
})
export class DiscountsHelperComponent implements OnInit {
  @Input() crudType: 'Create' | 'Update' = 'Create';
  @Input() discount!: Discount;
  private numberPattern = /^(100(?:\.0{1,2})?|[0-9]{1,2}(?:\.\d{1,2})?)$/;
  nameControl = new FormControl('', [Validators.required])
  percentControl = new FormControl(0, [Validators.required, Validators.pattern(this.numberPattern), Validators.min(0), Validators.max(100)])
  matcher = new GenericFormErrorStateMatcher()


  constructor(public dialogRef: MatDialogRef<CreateDiscountsPageComponent>,
    private discountService: DiscountsService,
              private errorHandler: ErrorHandlerService,
              private activatedRoute: ActivatedRoute) {
  }
  ngOnInit(): void {
      this.nameControl.setValue(this.discount.discountName);
      this.percentControl.setValue(this.discount.discountPercent);
  }

  onSubmit() {
    if (this.nameControl.invalid || this.percentControl.invalid) {
      return
    }
    const formdata = {
      discount_name: this.nameControl.value,
      discount_percent: this.percentControl.value,
      id: 0
    }
    if (this.crudType === 'Update') {
      formdata.id = this.discount.discountID;
      this.discountService.editDiscount(formdata).subscribe({
          next: () => {
            this.dialogRef.close();
            window.location.reload();
          },
          error: (error) => {
            this.errorHandler.handleError(error, "discounts/edit")
          }
        }
      )
    }


  }
}
