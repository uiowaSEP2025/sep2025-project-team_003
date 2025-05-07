import {Component, Input} from '@angular/core';
import {MatCard, MatCardTitle, MatCardContent, MatCardHeader, MatCardActions} from "@angular/material/card";
import {MatChip} from "@angular/material/chips";
import {RouterLink} from '@angular/router';
import {MatButton} from '@angular/material/button';

@Component({
  selector: 'app-services-card',
  standalone: true,
  imports: [
    MatCard,
    MatCardTitle,
    MatCardHeader,
    MatCardContent,
    MatCardActions,
    RouterLink,
    MatButton
  ],
  templateUrl: './services-card.component.html',
  styleUrl: './services-card.component.scss'
})
export class ServicesCardComponent {
  @Input() pageTitle = "";
  @Input() description = ""
  @Input() route!: string;


  protected readonly name = this.pageTitle;
}
