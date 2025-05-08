import { Component, OnInit } from '@angular/core';
import { OrganizationService } from '../../services/organization.service';
import {MENU_ITEMS} from '../../interfaces/menu.interface';
import {MenuInterface} from '../../interfaces/menu.interface';
import {ServicesCardComponent} from '../../components/services-card/services-card.component';
import {RouterLink} from '@angular/router';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';


@Component({
  selector: 'app-home-page',
  imports: [
    ServicesCardComponent,
    RouterLink,
    PageTemplateComponent
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {
  organization: any;

  menu_items = MENU_ITEMS;

  constructor(private organizationService: OrganizationService) {

  }

  ngOnInit(): void {
    this.organizationService.getOrganization().subscribe({
      next: (response) => {
        this.organization = response
      },
      error: (error) => {
      }
    })
  }
}
