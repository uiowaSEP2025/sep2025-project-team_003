import { Component } from '@angular/core';
import { PhoneNumberInputComponent } from '../phone-number-input/form-field-custom-control-example';

@Component({
  selector: 'app-test-component',
  imports: [PhoneNumberInputComponent],
  templateUrl: './test-component.component.html',
  styleUrl: './test-component.component.scss'
})
export class TestComponentComponent {

}
