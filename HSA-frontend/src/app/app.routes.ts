import { Routes } from '@angular/router';
import {HomePageComponent} from './pages/home-page/home-page.component';
import {TestPageComponent} from './pages/test-page/test-page.component';
import { LoginComponent } from './pages/login/login.component';

export const routes: Routes = [
  {
    path: '', component: HomePageComponent,
  },
  {
    path: 'home', component: HomePageComponent,
  },
  {
    path: 'test', component: TestPageComponent
  },
  {
    path: 'login', component: LoginComponent
  }
];
