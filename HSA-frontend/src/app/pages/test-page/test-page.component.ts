import { Component } from '@angular/core';
import { InternalInputManager } from '../../components/phone-number-input/phone-number-input-component';

@Component({
  selector: 'app-test-page',
  imports: [InternalInputManager],
  templateUrl: './test-page.component.html',
  styleUrl: './test-page.component.scss'
})
export class TestPageComponent {

}
