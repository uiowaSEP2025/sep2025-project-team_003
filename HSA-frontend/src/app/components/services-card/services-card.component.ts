import {Component, Input} from '@angular/core';
import {MatCard, MatCardTitle, MatCardContent, MatCardHeader, MatCardActions} from "@angular/material/card";
import {RouterLink} from "@angular/router";
import {MatButton} from '@angular/material/button';

@Component({
  selector: 'app-services-card',
  standalone: true,
  imports: [
    MatCard,
    MatCardTitle,
    MatCardHeader,
    MatCardContent,
    RouterLink,
    MatCardActions,
    MatButton,
  ],
  templateUrl: './services-card.component.html',
  styleUrl: './services-card.component.scss'
})
export class ServicesCardComponent {
  @Input() pageTitle = "";
  @Input() description = "";
  @Input() link = "";
}
