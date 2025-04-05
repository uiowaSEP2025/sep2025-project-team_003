import { Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { LoginComponent } from './pages/login/login.component';
import { ServicePageComponent } from './pages/services/service-page/service-page.component';
import { CustomersPageComponent } from './pages/customers/customers-page/customers-page.component';
import { CreateCustomerPageComponent } from './pages/customers/create-customer-page/create-customer-page.component';
import { EditCustomerPageComponent } from './pages/customers/edit-customer-page/edit-customer-page.component';
import { ContractorsPageComponent } from './pages/contractors/contractors-page/contractors-page.component';
import { EditContractorsPageComponent } from './pages/contractors/edit-contractors-page/edit-contractors-page.component';
import { CreateContractorsPageComponent } from './pages/contractors/create-contractors-page/create-contractors-page.component';
import { SignupPageComponent } from './pages/signup-page/signup-page.component';
import { CreateServicePageComponent } from './pages/services/create-service-page/create-service-page.component';
import { EditServicePageComponent } from './pages/services/edit-service-page/edit-service-page.component';
import { MaterialsPageComponent } from './pages/materials/materials-page/materials-page.component';
import { CreateMaterialPageComponent } from './pages/materials/create-material-page/create-material-page.component';
import { EditMaterialPageComponent } from './pages/materials/edit-material-page/edit-material-page.component';
import { InvoicesPageComponent } from './pages/invoices/invoices-page/invoices-page.component';
import { CreateInvoicePageComponent } from './pages/invoices/create-invoice-page/create-invoice-page.component';
import { ViewInvoicePageComponent } from './pages/invoices/view-invoice-page/view-invoice-page.component';
import { NotFoundPageComponent } from './pages/not-found-page/not-found-page.component';
import { EditInvoicePageComponent } from './pages/invoices/edit-invoice-page/edit-invoice-page.component';
import { JobPageComponent } from './pages/jobs/job-page/job-page.component';
import { ViewJobPageComponent } from './pages/jobs/view-job-page/view-job-page.component';
import { CreateJobPageComponent } from './pages/jobs/create-job-page/create-job-page.component';
import { EditJobPageComponent } from './pages/jobs/edit-job-page/edit-job-page.component';

export const routes: Routes = [
  {
    path: '', component: HomePageComponent,
  },
  {
    path: 'home', component: HomePageComponent,
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
    path: 'jobs', component: JobPageComponent
  },
  {
    path: 'job/:id', component: ViewJobPageComponent
  },
  {
    path: 'jobs/create', component: CreateJobPageComponent
  },
  {
    path: 'jobs/edit/:id', component: EditJobPageComponent
  },
  {
    path: 'invoices', component: InvoicesPageComponent
  },
  {
    path: 'invoices/create', component: CreateInvoicePageComponent
  },
  {
    path: 'invoice/:id', component: ViewInvoicePageComponent
  },
  {
    path: 'edit/invoice/:id', component: EditInvoicePageComponent
  },
  {
    path: '404',
    component: NotFoundPageComponent
  },
  {
    path: '**',
    component: NotFoundPageComponent
  }
];
