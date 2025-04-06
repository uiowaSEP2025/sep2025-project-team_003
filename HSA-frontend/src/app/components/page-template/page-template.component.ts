import {Component, inject, Input} from '@angular/core';
import {MatDivider} from '@angular/material/divider';
import {MatFabButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {MatDialog} from '@angular/material/dialog';
import {
  CreateContractorsPageComponent
} from '../../pages/contractors/create-contractors-page/create-contractors-page.component';

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
        { const dialogRef = this.dialog.open(CreateContractorsPageComponent)
        void dialogRef.afterClosed()
        }
    }
  }


}
