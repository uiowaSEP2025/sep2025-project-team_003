import { AbstractControl, ValidationErrors } from "@angular/forms";

export function passwordStrengthValidator(control: AbstractControl): ValidationErrors | null {
    const value = control.value;

    if (!value) {
      return null;
    }

    const hasUpperCase = /[A-Z]/.test(value);
    const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(value);

    if (!hasUpperCase) {
      return { passwordStrength: 'Must have 1 uppercase letter' } 
    }

    if (!hasSpecialChar) {
      return { passwordStrength: 'Must have 1 special character' } 
    }

    return null
  }

export function  passwordMatchValidator(form: AbstractControl): ValidationErrors | null {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
  
    if (password && confirmPassword && password !== confirmPassword) {
      form.get('confirmPassword')?.setErrors({ mismatch: true });

      return { mismatch: true };
    } else {
      form.get('confirmPassword')?.setErrors(null);

      return null;
    }
  }