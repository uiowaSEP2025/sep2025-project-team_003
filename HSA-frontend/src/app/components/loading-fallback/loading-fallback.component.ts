import { Component } from '@angular/core';
import { Input } from '@angular/core';

@Component({
  selector: 'app-loading-fallback',
  imports: [],
  templateUrl: './loading-fallback.component.html',
  styleUrl: './loading-fallback.component.scss'
})
export class LoadingFallbackComponent {
  @Input({required: true}) stringToDisplay = ''


}
