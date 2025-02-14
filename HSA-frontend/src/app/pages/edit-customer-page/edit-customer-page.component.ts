import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-edit-customer-page',
  imports: [],
  templateUrl: './edit-customer-page.component.html',
  styleUrl: './edit-customer-page.component.scss'
})
export class EditCustomerPageComponent {
  constructor(private activatedRoute: ActivatedRoute) {}

  ngOnInit() {
    console.log('init')
  this.activatedRoute.queryParams.subscribe(params => {
    const param1 = params['email'];
    const param2 = params['param2'];
    console.log(param1, param2); // Will print: value1 value2
  });}
  
}
