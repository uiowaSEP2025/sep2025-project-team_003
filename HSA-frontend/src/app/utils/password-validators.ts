import { AbstractControl, ValidationErrors } from "@angular/forms";

export function passwordStrengthValidator(control: AbstractControl): ValidationErrors | null {
	const value = control.value;

	const hasUpperCase = /[A-Z]/.test(value);
	const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(value);
	const hasNumber = /\d/.test(value);

	if (!hasUpperCase) {
	  return { passwordStrength: 'Must have 1 uppercase letter' };
	}

	if (!hasSpecialChar) {
	  return { passwordStrength: 'Must have 1 special character' };
	}

	if (!hasNumber) {
	  return { passwordStrength: 'Must have 1 number' };
	}

	return null;
  }

export function validateConfirmMatchesAndNotNull(form: AbstractControl): ValidationErrors | null {
	const password = form.get('password')?.value;
	const confirmPassword = form.get('confirmPassword')?.value;

	if (password !== confirmPassword) {
		form.get('confirmPassword')?.setErrors({ mismatch: true });
		return { mismatch: true };
	}
	else if (!confirmPassword) {
		form.get('confirmPassword')?.setErrors({ required: true });
		return null;
	}
	form.get('confirmPassword')?.setErrors(null);
	return null;
}
