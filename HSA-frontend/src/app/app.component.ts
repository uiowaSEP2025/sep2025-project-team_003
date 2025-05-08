import { Component } from '@angular/core';
import {HeaderComponent} from './layout/header/header.component';
import {BodyComponent} from './layout/body/body.component';
import {FooterComponent} from './layout/footer/footer.component';
import { NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs';
import {MenuInterface} from './interfaces/menu.interface';

@Component({
  selector: 'app-root',
  imports: [HeaderComponent, BodyComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'Handyman Services Application';


  constructor(private router: Router) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}
