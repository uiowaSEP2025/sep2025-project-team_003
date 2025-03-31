import { AbstractControl, ValidationErrors } from '@angular/forms';

export default function integerValidator(control: AbstractControl): ValidationErrors | null {
  const value = control.value;
  if (value === null || value === undefined || value === '') return null; // Allow empty values if needed
  if (!Number.isInteger(Number(value))) {
    return { notInteger: true };
  }
  return null;
}
