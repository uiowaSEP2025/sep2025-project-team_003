import { Component, OnInit } from '@angular/core';
import { MatToolbar } from '@angular/material/toolbar';
import { MatIcon } from '@angular/material/icon';
import { MatIconButton } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { UserAuthService } from '../../services/user-auth.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTooltip } from '@angular/material/tooltip';
import { OrganizationService } from '../../services/organization.service';
import { ErrorHandlerService } from '../../services/error.handler.service';

@Component({
  selector: 'app-header',
  imports: [
    MatToolbar,
    MatIcon,
    MatIconButton,
    MatTooltip,
    CommonModule
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent implements OnInit {
  sidebarExpanded = false;
  isLoggout = true

  constructor(private userAuth: UserAuthService, private router: Router, private snackBar: MatSnackBar) {}

  toggleSidebar() {
    this.sidebarExpanded = !this.sidebarExpanded
  }

  ngOnInit() {
    
  }

  onLogout() {
    this.userAuth.logout().subscribe({
      next: (response) => {
        this.snackBar.open('Logout successfully!', '', {
          duration: 3000
        });
        this.navigateToPage('login')
      },
      error: (error) => {
        this.snackBar.open('You are already logout!', '', {
          duration: 3000
        });
        this.isLoggout = true;
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]).then(() => {
      window.location.reload();
    });
  }
}
