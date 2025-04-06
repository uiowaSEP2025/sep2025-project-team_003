import { AbstractControl, AsyncValidatorFn, ValidationErrors } from '@angular/forms';
import { Observable, of } from 'rxjs';
import { delay, map } from 'rxjs/operators';

export function phoneValidator(): AsyncValidatorFn {
  return (control: AbstractControl): Observable<ValidationErrors | null> => {
    if (!control.value) {
      return of(null);
    }

    // Regular expression for xxx-xxx-xxxx format
    const phonePattern = /^\d{3}-\d{3}-\d{4}$/;

    // Simulate API call with delay
    return of(control.value).pipe(
      delay(100), // Simulate network delay
      map(value => {
        const valid = phonePattern.test(value);

        // You could add additional validation logic here
        // For example, checking if the phone number exists in a database

        return valid ? null : { invalidPhone: true };
      })
    );
  };
}
