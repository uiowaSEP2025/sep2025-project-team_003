import { Component } from '@angular/core';
import { MatToolbar } from '@angular/material/toolbar';
import { MatIcon } from '@angular/material/icon';
import { MatIconButton } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { UserAuthService } from '../../services/user-auth.service';

@Component({
  selector: 'app-header',
  imports: [
    MatToolbar,
    MatIcon,
    MatIconButton,
    CommonModule
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  sidebarExpanded = false;

  constructor(private userAuth: UserAuthService) {}

  toggleSidebar() {
    this.sidebarExpanded = !this.sidebarExpanded
  }

  onLogout() {
    this.userAuth.logout().subscribe({
      next: (response) => {
        console.log(response)
      },
      error: (error) => {

      }
    })
  }
}
