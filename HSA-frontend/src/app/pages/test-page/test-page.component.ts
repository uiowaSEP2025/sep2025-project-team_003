import { Component } from '@angular/core';
import { FormFieldCustomControl } from '../../components/phone-number-input/form-field-custom-control-example';

@Component({
  selector: 'app-test-page',
  imports: [FormFieldCustomControl],
  templateUrl: './test-page.component.html',
  styleUrl: './test-page.component.scss'
})
export class TestPageComponent {

}
