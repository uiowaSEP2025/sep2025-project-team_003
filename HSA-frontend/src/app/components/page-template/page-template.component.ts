import {Component, inject, Input} from '@angular/core';
import {MatDivider} from '@angular/material/divider';
import {MatFabButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {MatDialog} from '@angular/material/dialog';
import {
  CreateContractorPageComponent
} from '../../pages/contractors/create-contractors-page/create-contractor-page.component';
import {CreateCustomerPageComponent} from '../../pages/customers/create-customer-page/create-customer-page.component';
import {CreateMaterialPageComponent} from '../../pages/materials/create-material-page/create-material-page.component';
import {CreateServicePageComponent} from '../../pages/services/create-service-page/create-service-page.component';
import {CreateInvoicePageComponent} from '../../pages/invoices/create-invoice-page/create-invoice-page.component';

@Component({
  selector: 'app-page-template',
  imports: [
    MatDivider,
    MatFabButton,
    MatIcon
  ],
  templateUrl: './page-template.component.html',
  styleUrl: './page-template.component.scss'
})
export class PageTemplateComponent {
  @Input() title = '';
  readonly dialog = inject(MatDialog);

  openDialog() {
    switch (this.title) {
      case 'Contractors':
        { const dialogRef = this.dialog.open(CreateContractorPageComponent)
        void dialogRef.afterClosed()
        }
        break;
      case 'Customers':
      { const dialogRef = this.dialog.open(CreateCustomerPageComponent)
        void dialogRef.afterClosed()
      }
      break;
      case 'Materials':
      { const dialogRef = this.dialog.open(CreateMaterialPageComponent)
        void dialogRef.afterClosed()
      }
      break;
      case 'Services':
      { const dialogRef = this.dialog.open(CreateServicePageComponent)
        void dialogRef.afterClosed()
      }
        break;
      case 'Invoices':
      { const dialogRef = this.dialog.open(CreateInvoicePageComponent)
        void dialogRef.afterClosed()
      }
        break;
    }
  }


}
