import { Component } from '@angular/core';
import {MatDialogActions, MatDialogClose, MatDialogTitle} from "@angular/material/dialog";

@Component({
  selector: 'app-invoices-helper',
    imports: [
        MatDialogActions,
        MatDialogClose,
        MatDialogTitle
    ],
  templateUrl: './invoices-helper.component.html',
  styleUrl: './invoices-helper.component.scss'
})
export class InvoicesHelperComponent {

}
