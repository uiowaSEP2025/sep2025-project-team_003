import { Component, OnInit } from '@angular/core';
import { OrganizationService } from '../../../services/organization.service';

@Component({
  selector: 'app-home-page',
  imports: [],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {
  organization: any;

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
