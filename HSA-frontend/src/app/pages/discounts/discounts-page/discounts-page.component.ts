import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../../components/table-component/table-component.component';
import { Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { LoadingFallbackComponent } from '../../../components/loading-fallback/loading-fallback.component';
import { DiscountsService } from '../../../services/discount.service';
import { ErrorHandlerService } from '../../../services/error.handler.service';
import { MatButtonModule } from '@angular/material/button';
import {PageTemplateComponent} from '../../../components/page-template/page-template.component';
import {TableApiResponse} from '../../../interfaces/api-responses/table.api.interface';
import {Discount} from '../../../interfaces/discount.interface';

@Component({
  selector: 'app-discounts-page',
  imports: [TableComponentComponent, MatIconModule, LoadingFallbackComponent, MatButtonModule, PageTemplateComponent],
  templateUrl: './discounts-page.component.html',
  styleUrl: './discounts-page.component.scss'
})
export class DiscountsPageComponent implements OnInit{
  discounts: TableApiResponse<Discount> = {
    data: [],
    totalCount: 0
  }
  discountService: DiscountsService
  loading = false;


  constructor (private router: Router, discountService: DiscountsService, private errorHandler: ErrorHandlerService) {
    this.discountService = discountService
  }

  ngOnInit(): void {
    void this.loadDataToTable("", 5, 0);
  }

  async loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.loading = true;
    this.discountService.getDiscounts({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.discounts = response
        this.loading = false;
      },
      error: (error) => {
          this.errorHandler.handleError(error, 'discounts')
        this.loading = false;
      }
    })
  }


}
