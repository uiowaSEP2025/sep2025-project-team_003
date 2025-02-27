import { Component, OnInit, ViewChild } from '@angular/core';
import {Router} from '@angular/router';
import {MatFabButton} from '@angular/material/button';
import {MatIcon} from '@angular/material/icon';
import {TableComponentComponent} from '../../components/table-component/table-component.component';
import { MaterialService } from '../../services/material.service';

@Component({
  selector: 'app-materials-page',
  imports: [
    MatFabButton,
    MatIcon,
    TableComponentComponent
  ],
  templateUrl: './materials-page.component.html',
  styleUrl: './materials-page.component.scss'
})
export class MaterialsPageComponent implements OnInit {
  materials: any
  materialService: MaterialService
  @ViewChild(TableComponentComponent) tableComponent!: TableComponentComponent 

  constructor(private router: Router, materialService: MaterialService) {
    this.materialService = materialService
  }
  

  ngOnInit(): void {
    this.loadDataToTable("", 20, 0);
  }

  loadDataToTable(searchTerm: string, pageSize: number, offSet: number) {
    this.materialService.getMaterial({ search: searchTerm, pagesize: pageSize, offset: offSet}).subscribe({
      next: (response) => {
        this.materials = response
      },
      error: (error) => {
        
      }
    })
  }

  onPageChange(event: { searchTerm: string; pageSize: number; offset: number }): void {
    this.loadDataToTable(event.searchTerm, event.pageSize, event.offset);
  }
  

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]).then(() => {
      window.location.reload();
    });
  }
}
