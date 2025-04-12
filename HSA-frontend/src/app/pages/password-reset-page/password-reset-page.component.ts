import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ReactiveFormsModule, Validators } from '@angular/forms';
import { MatInputModule, MatError } from '@angular/material/input';


@Component({
  selector: 'app-password-reset-page',
  imports: [ReactiveFormsModule, MatInputModule, MatError],
  templateUrl: './password-reset-page.component.html',
  styleUrl: './password-reset-page.component.scss'
})
export class PasswordResetPageComponent implements OnInit{

  private token!:string

  constructor(private activatedRoute: ActivatedRoute) {}



  ngOnInit(): void {
    this.activatedRoute.queryParams.subscribe(params => {
      this.token = params['token'];
    });
  }

  onSubmit() {

  }

}
