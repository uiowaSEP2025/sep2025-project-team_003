import {Component, Input} from '@angular/core';
import {MatDivider} from "@angular/material/divider";

@Component({
  selector: 'app-page-template',
  standalone: true,
    imports: [
        MatDivider
    ],
  templateUrl: './page-template.component.html',
  styleUrl: './page-template.component.scss'
})
export class PageTemplateComponent {
  @Input() title = '';

}
