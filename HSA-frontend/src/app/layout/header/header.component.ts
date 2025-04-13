import { Component, OnInit } from '@angular/core';
import { MatToolbar } from '@angular/material/toolbar';
import { MatIcon } from '@angular/material/icon';
import { MatIconButton } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { UserAuthService } from '../../services/user-auth.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTooltip } from '@angular/material/tooltip';
import { Subscription } from 'rxjs';

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
  isLoggedIn: boolean = false; 
  private loginStatusSubscription: Subscription = new Subscription();


  constructor(private userAuth: UserAuthService, private router: Router, private snackBar: MatSnackBar) {}

  toggleSidebar() {
    this.sidebarExpanded = !this.sidebarExpanded
  }
  ngOnInit() {
    this.loginStatusSubscription = this.userAuth.isLoggedIn$.subscribe((status) => {
      this.isLoggedIn = status; // Update local status when the login status changes
    });
  }

  onLogout() {
    this.userAuth.logout().subscribe({
      next: (response) => {
        this.snackBar.open('Logout successfully!', '', {
          duration: 3000
        });
        this.isLoggedIn = false
        this.userAuth.setLoginStatus(false)
        this.navigateToPage('login')
      },
      error: (error) => {
        this.snackBar.open('You are already logout!', '', {
          duration: 3000
        });
        
      }
    })
  }


  ngOnDestroy() {
    // Unsubscribe from observable to avoid memory leaks
    if (this.loginStatusSubscription) {
      this.loginStatusSubscription.unsubscribe();
    }
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`])
  }
}
