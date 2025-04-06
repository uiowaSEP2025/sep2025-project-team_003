import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';

@Component({
  selector: 'app-discounts-page',
  imports: [],
  templateUrl: './discounts-page.component.html',
  styleUrl: './discounts-page.component.scss'
})
export class DiscountsPageComponent implements OnInit{

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    // this.customerService.getCustomer({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
    //   next: (response) => {
    //     this.customers = response
    //   },
    //   error: (error) => {
    //       this.errorHandler.handleError(error, 'customers')
    //   }
    // })
  }

}
