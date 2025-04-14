import {Component} from '@angular/core';
import {HeaderComponent} from './layout/header/header.component';
import {BodyComponent} from './layout/body/body.component';
import {FooterComponent} from './layout/footer/footer.component';
import {MatDrawer, MatDrawerContainer, MatDrawerContent} from "@angular/material/sidenav";
import {MatListItem, MatNavList} from '@angular/material/list';
import {MenuInterface} from './interfaces/menu.interface';
import {RouterLink, RouterLinkActive} from '@angular/router';
import {MatIcon} from '@angular/material/icon';
import {MatLabel} from '@angular/material/form-field';
import { NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [HeaderComponent, BodyComponent, FooterComponent, MatDrawer, MatDrawerContainer, MatDrawerContent,
    MatListItem, MatNavList, RouterLink, RouterLinkActive, MatIcon, MatLabel],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'HSA-frontend';


  menuItems: MenuInterface[] = [
    {name: 'Home', route: '/home'},
    {name: 'Customers', route: '/customers'},
    {name: 'Contractors', route: '/contractors'},
    {name: 'Services', route: '/services'},
    {name: 'Jobs', route: '/jobs'},
    {name: 'Materials', route: '/materials'},
    {name: 'Invoices', route: '/invoices'},
    {name: 'Discounts', route: '/discounts'},
  ]

  constructor(private router: Router) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}
