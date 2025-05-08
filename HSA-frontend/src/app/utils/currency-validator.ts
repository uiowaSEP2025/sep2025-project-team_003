import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function currencyValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;

    if (value === null || value === undefined || value === '') {
      return null; // Let required validator handle empty values
    }

    const currencyRegex = /^\d+(\.\d{2})?$/;

    return currencyRegex.test(value) ? null : { invalidCurrency: true };
  };
}