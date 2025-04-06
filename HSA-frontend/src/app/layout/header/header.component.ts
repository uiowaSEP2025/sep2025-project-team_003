import {Component, Input} from '@angular/core';
import { MatToolbar } from '@angular/material/toolbar';
import { MatIcon } from '@angular/material/icon';
import {MatIconButton} from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { UserAuthService } from '../../services/user-auth.service';
import {Router} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import {MatDrawer} from '@angular/material/sidenav';

@Component({
  selector: 'app-header',
  imports: [
    MatToolbar,
    MatIcon,
    MatIconButton,
    CommonModule,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  @Input() drawer: MatDrawer;

  constructor(private userAuth: UserAuthService, private router: Router, private snackBar: MatSnackBar) {
    this.drawer = new MatDrawer();
  }

  toggle() {
    void this.drawer.toggle()
  }

  onLogout() {
    this.userAuth.logout()
  }
}
