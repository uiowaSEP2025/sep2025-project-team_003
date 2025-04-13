import { ChangeDetectionStrategy, Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { AbstractControl, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButton } from '@angular/material/button';
import { MatOption, MatSelect } from '@angular/material/select';
import { HttpClient} from '@angular/common/http';
import { StateList } from '../../utils/states-list';
import { UserAuthService } from '../../services/user-auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationService } from '../../services/organization.service';
import { RequestTrackerService } from '../../utils/request-tracker';
import { MatCardModule } from '@angular/material/card';
import { passwordStrengthValidator, validateConfirmMatchesAndNotNull } from '../../utils/password-validators';

@Component({
  selector: 'app-signup-page',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatStepperModule,
    MatCardModule,
    FormsModule,
    ReactiveFormsModule,
    MatButton,
    MatSelect,
    MatOption
  ],
  templateUrl: './signup-page.component.html',
  styleUrl: './signup-page.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})

export class SignupPageComponent {
  userAccountForm: FormGroup;
  registrationForm: FormGroup;
  organizationLocationForm: FormGroup;
  states: any = []
  @ViewChild('stepper') stepper!: MatStepper;

  constructor(
    private router: Router, 
    private userAccountFormBuilder: FormBuilder,
    private registrationFormBuilder: FormBuilder, 
    private organizationLocationFormBuilder: FormBuilder,
    private authService: UserAuthService, 
    private organizationService: OrganizationService,
    private tracker: RequestTrackerService,
    private snackBar: MatSnackBar,
    private http: HttpClient,
  ) {
    this.userAccountForm = this.userAccountFormBuilder.group({
      userFirstName: ['', Validators.required],
      userLastName: ['', Validators.required],
      userEmail: ['', [Validators.required, Validators.email]],
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(16), passwordStrengthValidator]],
      confirmPassword: ['', Validators.required],
    }, {validators: validateConfirmMatchesAndNotNull});

    this.registrationForm = this.registrationFormBuilder.group({
      organizationName: ['', Validators.required],
      organizationEmail: ['', [Validators.required, Validators.email]],
      organizationPhone: ['', Validators.required],
      ownerName: ['', Validators.required],
    });

    this.organizationLocationForm = this.organizationLocationFormBuilder.group({
      addressOne: ['', Validators.required],
      city: ['', Validators.required],
      zipCode: ['', Validators.required],
      stateSelect: ['', Validators.required],
    })

    this.states = StateList.getStates()
  }

  onSubmitUserCreation() {
    if (this.userAccountForm.invalid) {
      this.userAccountForm.markAllAsTouched();
    } else {
      const userExistRequest = {
        username: this.userAccountForm.get('username')?.value,
        password: this.userAccountForm.get('password')?.value
      }

      this.authService.checkUserExist(userExistRequest).subscribe({
        next: (response) => {
          this.stepper.selected!.completed = true;
          this.stepper.next();

          this.registrationForm.patchValue({
            organizationEmail: this.userAccountForm.get('userEmail')?.value,
            ownerName: this.userAccountForm.get('userFirstName')?.value + ' ' + this.userAccountForm.get('userLastName')?.value
          });
        },
        error: (error) => {
          this.snackBar.open('Username is already registered, please change username or login', '', {
            duration: 3000
          });
          this.stepper.selected!.completed = false;
        }
      })
    }
  }

  onSubmitRegistration() {
    if (this.registrationForm.invalid) {
      this.registrationForm.markAllAsTouched();
      return;
    } else {
      this.tracker.startRequest();
     
     
      const organizationCreateRequest = {
        name: this.registrationForm.get('organizationName')?.value,
        email: this.registrationForm.get('organizationEmail')?.value,
        city: this.organizationLocationForm.get('city')?.value,
        phone: this.registrationForm.get('organizationPhone')?.value,
        requestorState: this.organizationLocationForm.get('stateSelect')?.value,
        requestorZip: this.organizationLocationForm.get('zipCode')?.value,
        requestorAddress: this.organizationLocationForm.get('addressOne')?.value,
        ownerFn: this.registrationForm.get('ownerName')?.value.split(' ')[0],
        ownerLn: this.registrationForm.get('ownerName')?.value.split(' ').slice(1).join(' '),
        isOnboarding: true,
      }
 
      const userCreateRequest = {
        organizationInfo: organizationCreateRequest,
        firstName: this.userAccountForm.get('userFirstName')?.value,
        lastName: this.userAccountForm.get('userLastName')?.value,
        email: this.userAccountForm.get('userEmail')?.value,
        username: this.userAccountForm.get('username')?.value,
        password: this.userAccountForm.get('password')?.value
      }
 
      this.authService.createUser(userCreateRequest).subscribe({
        next: (response) => {
          this.snackBar.open('Organization Created!', '', {
            duration: 3000
          });
          this.router.navigate(["login"])
        },
        error: (error) => {
 
        }
      })
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
