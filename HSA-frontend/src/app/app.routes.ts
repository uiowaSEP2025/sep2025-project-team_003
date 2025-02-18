import { Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { TestPageComponent } from './pages/test-page/test-page.component';
import { LoginComponent } from './pages/login/login.component';
<<<<<<< HEAD
=======
import { ServicePageComponent } from './pages/service-page/service-page.component';
>>>>>>> 762b519 (HSA 26 add route to services)
import { CustomersPageComponent } from './pages/customers-page/customers-page.component';
import { CreateCustomerPageComponent } from './pages/create-customer-page/create-customer-page.component';
import { EditCustomerPageComponent } from './pages/edit-customer-page/edit-customer-page.component';
import { ContractorsPageComponent } from './pages/contractors-page/contractors-page.component';
import { EditContractorsPageComponent } from './pages/edit-contractors-page/edit-contractors-page.component';
import { CreateContractorsPageComponent } from './pages/create-contractors-page/create-contractors-page.component';
<<<<<<< HEAD
import {SignupPageComponent} from './pages/signup-page/signup-page.component';
import {ServicePageComponent} from './pages/service-page/service-page.component';

=======
import { CreateServicePageComponent } from './pages/create-service-page/create-service-page.component';
import { EditServicePageComponent } from './pages/edit-service-page/edit-service-page.component';
<<<<<<< HEAD
>>>>>>> 762b519 (HSA 26 add route to services)
=======
import {MaterialsPageComponent} from './pages/materials-page/materials-page.component';
import {CreateMaterialPageComponent} from './pages/create-material-page/create-material-page.component';
import {EditMaterialPageComponent} from './pages/edit-material-page/edit-material-page.component';
>>>>>>> eb2a7f7 (HSA 27 Add pages for material and tests.)

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
<<<<<<< HEAD
=======
    path: 'services', component: ServicePageComponent
  },
  {
    path: 'services/create', component: CreateServicePageComponent
  },
  {
    path: 'services/edit/:id', component: EditServicePageComponent
  },
  {
<<<<<<< HEAD
>>>>>>> 762b519 (HSA 26 add route to services)
=======
    path: 'materials', component: MaterialsPageComponent
  },
  {
    path: 'materials/create', component: CreateMaterialPageComponent
  },
  {
    path: 'materials/edit/:id', component: EditMaterialPageComponent
  },
  {
>>>>>>> eb2a7f7 (HSA 27 Add pages for material and tests.)
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
  {
    path: 'service', component: ServicePageComponent
  }

];
