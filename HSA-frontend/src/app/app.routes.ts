import { Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { TestPageComponent } from './pages/test-page/test-page.component';
import { LoginComponent } from './pages/login/login.component';
import { CustomersPageComponent } from './pages/customers-page/customers-page.component';
import { CreateCustomerPageComponent } from './pages/create-customer-page/create-customer-page.component';
import { EditCustomerPageComponent } from './pages/edit-customer-page/edit-customer-page.component';
import { SignupPageComponent } from './pages/signup-page/signup-page.component';
import { ContractorsPageComponent } from './pages/contractors-page/contractors-page.component';
import { EditContractorsPageComponent } from './pages/edit-contractors-page/edit-contractors-page.component';
import { CreateContractorsPageComponent } from './pages/create-contractors-page/create-contractors-page.component';

export const routes: Routes = [
  {
    path: '', component: HomePageComponent,
  },
  {
    path: 'home', component: HomePageComponent,
  },
  {
    path: 'test', component: TestPageComponent,
  },
  {
    path: 'signup', component: SignupPageComponent,
  },
  {
    path: 'login', component: LoginComponent
  },
  {
    path: 'customers', component: CustomersPageComponent
  },
  {
    path: 'customers/create', component: CreateCustomerPageComponent
  },
  {
    path: 'customers/edit/:id', component: EditCustomerPageComponent
  },
  {
    path: 'contractors', component: ContractorsPageComponent
  },
  {
    path: 'contractors/edit/:id', component: EditContractorsPageComponent
  },
  {
    path: 'contractors/create', component: CreateContractorsPageComponent 
  },
];
