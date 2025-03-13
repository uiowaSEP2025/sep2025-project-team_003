import { Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { TestPageComponent } from './pages/test-page/test-page.component';
import { LoginComponent } from './pages/login/login.component';
import { ServicePageComponent } from './pages/service-page/service-page.component';
import { CustomersPageComponent } from './pages/customers-page/customers-page.component';
import { CreateCustomerPageComponent } from './pages/create-customer-page/create-customer-page.component';
import { EditCustomerPageComponent } from './pages/edit-customer-page/edit-customer-page.component';
import { ContractorsPageComponent } from './pages/contractors-page/contractors-page.component';
import { EditContractorsPageComponent } from './pages/edit-contractors-page/edit-contractors-page.component';
import { CreateContractorsPageComponent } from './pages/create-contractors-page/create-contractors-page.component';
import {SignupPageComponent} from './pages/signup-page/signup-page.component';
import { CreateServicePageComponent } from './pages/create-service-page/create-service-page.component';
import { EditServicePageComponent } from './pages/edit-service-page/edit-service-page.component';
import {MaterialsPageComponent} from './pages/materials-page/materials-page.component';
import {CreateMaterialPageComponent} from './pages/create-material-page/create-material-page.component';
import {EditMaterialPageComponent} from './pages/edit-material-page/edit-material-page.component';
import { CreateJobsPageComponent } from './pages/create-jobs-page/create-jobs-page.component';
import { InvoicesPageComponent } from './pages/invoices-page/invoices-page.component';
import { CreateInvoicePageComponent } from './pages/create-invoice-page/create-invoice-page.component';
import { ViewInvoicePageComponent } from './pages/view-invoice-page/view-invoice-page.component';
import { NotFoundPageComponent } from './pages/not-found-page/not-found-page.component';

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
    path: 'services', component: ServicePageComponent
  },
  {
    path: 'services/create', component: CreateServicePageComponent
  },
  {
    path: 'services/edit/:id', component: EditServicePageComponent
  },
  {
    path: 'materials', component: MaterialsPageComponent
  },
  {
    path: 'materials/create', component: CreateMaterialPageComponent
  },
  {
    path: 'materials/edit/:id', component: EditMaterialPageComponent
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
  {
    path: 'services', component: ServicePageComponent
  }, 
  {
    path: 'jobs/create', component: CreateJobsPageComponent
  }, 
  {
    path: 'invoices', component: InvoicesPageComponent
  }, 
  {
    path: 'invoices/create', component: CreateInvoicePageComponent
  }, 
  { 
    path: '**', 
    component: NotFoundPageComponent // or redirectTo: 'some-default-route'
  }
];
