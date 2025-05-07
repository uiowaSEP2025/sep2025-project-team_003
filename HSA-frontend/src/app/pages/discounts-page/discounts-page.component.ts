import { Component, OnInit } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { DiscountsService } from '../../services/discount.service';
import { MatButtonModule } from '@angular/material/button';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';

@Component({
  selector: 'app-discounts-page',
  imports: [TableComponentComponent, MatIconModule, LoadingFallbackComponent, MatButtonModule, PageTemplateComponent],
  templateUrl: './discounts-page.component.html',
  styleUrl: './discounts-page.component.scss'
})
export class DiscountsPageComponent implements OnInit{
  discounts: any = null
  discountService: DiscountsService


  constructor (private router: Router, discountService: DiscountsService) {
    this.discountService = discountService
  }

  ngOnInit(): void {
    this.loadDataToTable("", 5, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.discountService.getDiscounts({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.discounts = response
      },
      error: (error) => {
      }
    })
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }

}
