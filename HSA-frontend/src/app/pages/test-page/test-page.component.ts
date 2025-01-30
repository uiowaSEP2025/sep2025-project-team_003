import { Component } from '@angular/core';
import {MatIcon} from '@angular/material/icon';
import {
  MatAnchor,
  MatButton,
  MatFabAnchor,
  MatFabButton,
  MatIconButton,
  MatMiniFabButton
} from '@angular/material/button';
import {RouterLink} from '@angular/router';
import {MatDivider} from '@angular/material/divider';

@Component({
  selector: 'app-test-page',
  imports: [
    MatIcon,
    MatMiniFabButton,
    MatFabButton,
    MatFabAnchor,
    RouterLink,
    MatDivider,
    MatButton,
    MatAnchor,
    MatIconButton
  ],
  templateUrl: './test-page.component.html',
  styleUrl: './test-page.component.scss'
})
export class TestPageComponent {

}
