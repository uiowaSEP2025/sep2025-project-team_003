import { Component, Input } from '@angular/core';




@Component({
  selector: 'app-invoice-job',
  imports: [],
  templateUrl: './invoice-job.component.html',
  styleUrl: './invoice-job.component.scss'
})
export class InvoiceJobComponent {
  @Input() data: any = null
}
