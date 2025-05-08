import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTableModule } from '@angular/material/table';
import { CalendarComponentComponent } from "../../components/calendar-component/calendar-component.component";
import { ContractorService } from '../../services/contractor.service';
import { MatSelectModule } from '@angular/material/select';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { ContractorNameId } from '../../services/contractor.service';
import {PageTemplateComponent} from '../../components/page-template/page-template.component';

@Component({
  selector: 'app-booking-page',
  imports: [
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    ReactiveFormsModule,
    CommonModule,
    MatTableModule,
    MatCardModule,
    CalendarComponentComponent,
    MatSelectModule,
    LoadingFallbackComponent,
    PageTemplateComponent
  ],
  templateUrl: './booking-page.component.html',
  styleUrl: './booking-page.component.scss'
})
export class BookingPageComponent implements OnInit {
  contractors: ContractorNameId[] | null = null

  ngOnInit(): void {
    this.contractorService.getAllContractors().subscribe({
      next: (res: any) => {
        this.contractors = res
      }
    })
  }

  constructor(private contractorService: ContractorService) {

  }
}
