import { Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { LoginComponent } from './pages/login/login.component';
import { ServicePageComponent } from './pages/service-page/service-page.component';
import { CustomersPageComponent } from './pages/customers-page/customers-page.component';
import { CreateCustomerPageComponent } from './pages/create-customer-page/create-customer-page.component';
import { EditCustomerPageComponent } from './pages/edit-customer-page/edit-customer-page.component';
import { ContractorsPageComponent } from './pages/contractors-page/contractors-page.component';
import { EditContractorsPageComponent } from './pages/edit-contractors-page/edit-contractors-page.component';
import { CreateContractorsPageComponent } from './pages/create-contractors-page/create-contractors-page.component';
import { SignupPageComponent } from './pages/signup-page/signup-page.component';
import { CreateServicePageComponent } from './pages/create-service-page/create-service-page.component';
import { EditServicePageComponent } from './pages/edit-service-page/edit-service-page.component';
import { MaterialsPageComponent } from './pages/materials-page/materials-page.component';
import { CreateMaterialPageComponent } from './pages/create-material-page/create-material-page.component';
import { EditMaterialPageComponent } from './pages/edit-material-page/edit-material-page.component';
import { InvoicesPageComponent } from './pages/invoices-page/invoices-page.component';
import { CreateInvoicePageComponent } from './pages/create-invoice-page/create-invoice-page.component';
import { ViewInvoicePageComponent } from './pages/view-invoice-page/view-invoice-page.component';
import { NotFoundPageComponent } from './pages/not-found-page/not-found-page.component';
import { EditInvoicePageComponent } from './pages/edit-invoice-page/edit-invoice-page.component';
import { JobPageComponent } from './pages/job-page/job-page.component';
import { ViewJobPageComponent } from './pages/view-job-page/view-job-page.component';
import { CreateJobPageComponent } from './pages/create-job-page/create-job-page.component';
import { EditJobPageComponent } from './pages/edit-job-page/edit-job-page.component';
import { DiscountsPageComponent } from './pages/discounts-page/discounts-page.component';
import { CreateDiscountsPageComponent } from './pages/create-discounts-page/create-discounts-page.component';
import { EditDiscountPageComponent } from './pages/edit-discount-page/edit-discount-page.component';
import { OnboardingPageComponent } from './pages/onboarding-page/onboarding-page.component';
import { Error500PageComponent } from './pages/error-500-page/error-500-page.component';
import { RequestPasswordResetPageComponent } from './pages/request-password-reset-page/request-password-reset-page.component';
import { PasswordResetPageComponent } from './pages/password-reset-page/password-reset-page.component';
import { BookingPageComponent } from './pages/booking-page/booking-page.component';


export const routes: Routes = [
  {
    path: '',
    children: [
      {
        path: 'home', component: HomePageComponent,
      },
      {
        path: 'onboarding', component: OnboardingPageComponent
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
        path: "discounts", component: DiscountsPageComponent 
      },
      {
        path: "discounts/create", component: CreateDiscountsPageComponent
      },
      {
        path: 'discounts/edit/:id', component: EditDiscountPageComponent
      },
      {
        path: 'booking', component: BookingPageComponent
      },
    ]
  },
  
  
  {
    path: 'signup', component: SignupPageComponent,
  },
  {
    path: 'login', component: LoginComponent
  },
  {
    path: 'password/reset/confirmation', component: PasswordResetPageComponent
  },
  {
    path: 'password/reset', component: RequestPasswordResetPageComponent
  },
  {
    path: '404',
    component: NotFoundPageComponent
  },
  {
    path: '500',
    component: Error500PageComponent
  },
  {
    path: '**',
    component: NotFoundPageComponent
  }
];
