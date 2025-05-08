import { Component } from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import {Router, RouterLink} from '@angular/router';

@Component({
  selector: 'app-not-found-page',
  imports: [MatCardModule, MatButtonModule, MatIconModule, RouterLink],
  templateUrl: './not-found-page.component.html',
  styleUrl: './not-found-page.component.scss'
})
export class NotFoundPageComponent {

  constructor (private router: Router) {}

  goHome() {
    this.router.navigate(['/'])
  }

}
