import { Routes } from '@angular/router';
import { HomePageComponent } from './pages/general/home-page/home-page.component';
import { LoginComponent } from './pages/authentication/login/login.component';
import { ServicePageComponent } from './pages/services/service-page/service-page.component';
import { CustomersPageComponent } from './pages/customers/customers-page/customers-page.component';
import { CreateCustomerPageComponent } from './pages/customers/create-customer-page/create-customer-page.component';
import { EditCustomerPageComponent } from './pages/customers/edit-customer-page/edit-customer-page.component';
import { ContractorsPageComponent } from './pages/contractors/contractors-page/contractors-page.component';
import { EditContractorsPageComponent } from './pages/contractors/edit-contractors-page/edit-contractors-page.component';
import { CreateContractorsPageComponent } from './pages/contractors/create-contractors-page/create-contractors-page.component';
import { SignupPageComponent } from './pages/general/signup-page/signup-page.component';
import { CreateServicePageComponent } from './pages/services/create-service-page/create-service-page.component';
import { EditServicePageComponent } from './pages/services/edit-service-page/edit-service-page.component';
import { MaterialsPageComponent } from './pages/materials/materials-page/materials-page.component';
import { CreateMaterialPageComponent } from './pages/materials/create-material-page/create-material-page.component';
import { EditMaterialPageComponent } from './pages/materials/edit-material-page/edit-material-page.component';
import { InvoicesPageComponent } from './pages/invoices/invoices-page/invoices-page.component';
import { CreateInvoicePageComponent } from './pages/invoices/create-invoice-page/create-invoice-page.component';
import { ViewInvoicePageComponent } from './pages/invoices/view-invoice-page/view-invoice-page.component';
import { NotFoundPageComponent } from './pages/general/not-found-page/not-found-page.component';
import { EditInvoicePageComponent } from './pages/invoices/edit-invoice-page/edit-invoice-page.component';
import { JobPageComponent } from './pages/jobs/job-page/job-page.component';
import { ViewJobPageComponent } from './pages/jobs/view-job-page/view-job-page.component';
import { CreateJobPageComponent } from './pages/jobs/create-job-page/create-job-page.component';
import { EditJobPageComponent } from './pages/jobs/edit-job-page/edit-job-page.component';
import { DiscountsPageComponent } from './pages/discounts/discounts-page/discounts-page.component';
import { CreateDiscountsPageComponent } from './pages/discounts/create-discounts-page/create-discounts-page.component';
import { EditDiscountPageComponent } from './pages/discounts/edit-discount-page/edit-discount-page.component';
import { OnboardingPageComponent } from './pages/general/onboarding-page/onboarding-page.component';
import { Error500PageComponent } from './pages/general/error-500-page/error-500-page.component';
import { RequestPasswordResetPageComponent } from './pages/authentication/request-password-reset-page/request-password-reset-page.component';
import { PasswordResetPageComponent } from './pages/authentication/password-reset-page/password-reset-page.component';
import { BookingPageComponent } from './pages/bookings/booking-page/booking-page.component';
import { QuoteSignComponent } from './pages/quote-sign/quote-sign.component'
import { QuotesDashboardPageComponent } from './pages/quotes-dashboard-page/quotes-dashboard-page.component';
import { RequestDashboardPageComponent } from './pages/request-dashboard-page/request-dashboard-page.component';

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
      {
        path: 'signquote', component: QuoteSignComponent
      },
      {
        path: 'quotes', component: QuotesDashboardPageComponent
      },
      {
        path: 'requests', component: RequestDashboardPageComponent
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
