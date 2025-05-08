import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import {Router, RouterLink} from '@angular/router';

@Component({
  selector: 'app-error-500-page',
  imports: [MatCardModule, MatButtonModule, MatIconModule, RouterLink],
  templateUrl: './error-500-page.component.html',
  styleUrl: './error-500-page.component.scss'
})
export class Error500PageComponent {

  constructor (private router: Router) {}

  goHome() {
    this.router.navigate(['/'])
  }

}
