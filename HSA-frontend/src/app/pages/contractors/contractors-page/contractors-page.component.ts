import {Component} from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import {PageTemplateComponent} from '../../../components/page-template/page-template.component';
import {DataTableComponent} from '../../../components/data-table/data-table.component';
import {finalize} from 'rxjs';
import {ContractorService} from '../../../services/contractor.service';

@Component({
  selector: 'app-contractors-page',
  imports: [MatButtonModule, CommonModule, PageTemplateComponent, DataTableComponent],
  templateUrl: './contractors-page.component.html',
  styleUrl: './contractors-page.component.scss'
})
export class ContractorsPageComponent  {
  isTableLoading = false;
  private _contractorService: ContractorService;

  constructor(contractorService: ContractorService) {
    this._contractorService = contractorService;

  }

  onEdit(row: any) {
    this.isTableLoading = true;
    // Perform edit operation
    this.dataService.editItem(row).pipe(
      finalize(() => {
        this.isTableLoading = false;
      })
    ).subscribe({
      next: (response) => {
        // Handle success
      },
      error: (error) => {
        // Handle error
      }
    });
  }

  onDelete(row: any) {
    this.isTableLoading = true;
    this.yourService.deleteItem(row.id).pipe(
      finalize(() => {
        this.isTableLoading = false;
      })
    ).subscribe({
      next: () => {
        // Refresh table or remove row
      },
      error: (error) => {
        // Handle error
      }
    });
  }
}
