import { Component } from '@angular/core';
import { TableComponentComponent } from '../../components/table-component/table-component.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIcon } from '@angular/material/icon';
import { Router } from '@angular/router';
import { ContractorService } from '../../services/contractor.service';

@Component({
  selector: 'app-contractors-page',
  imports: [TableComponentComponent, MatButtonModule, MatIcon],
  templateUrl: './contractors-page.component.html',
  styleUrl: './contractors-page.component.scss'
})
export class ContractorsPageComponent {
  contractorService: ContractorService

  constructor(private router: Router, contractorService: ContractorService) {
    this.contractorService = contractorService
  }

  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
