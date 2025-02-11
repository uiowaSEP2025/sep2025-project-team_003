import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { MatIconModule } from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';


// TODO: for data fetching, add a service: https://stackademic.com/blog/fetching-data-from-an-api-in-angular
@Component({
  selector: 'app-table-component',
  imports: [MatTableModule, MatPaginatorModule, MatInputModule, MatSelectModule, ReactiveFormsModule,MatIconModule,MatButtonModule],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit {
  searchControl = new FormControl('')
  page:number | null = null // null when unspecified
  pageSize:number | null = null // null when unspecified
  headers = ['header1', 'header2', 'header3', 'header4']
  headersWithActions = [...this.headers, 'actions']
  data = new MatTableDataSource(rows)
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  refetchData(searchTerm: string | null) {
    // TODO: fix it in service ticket, add a mock in the test to ensure that it only fetches when valid
    console.log(`Fetching data with search term: ${searchTerm}
      pageSize: ${this.pageSize}, pageIndex: ${this.page}`);
  }

  ngAfterViewInit() {
    this.data.paginator = this.paginator;
    this.searchControl.valueChanges
      .pipe(
        debounceTime(300), // Wait for 300ms after the last change
        distinctUntilChanged() // Only emit if the value has changed
      )
      .subscribe((searchTerm) => {
        this.refetchData(searchTerm);
      });

      console.log(this.headersWithActions)
    
      this.paginator.page.subscribe((page) => {
        this.page = page.pageIndex;
        this.pageSize = page.pageSize;
        this.refetchData(this.searchControl.value);
      })}
}

const rows = [
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' },
  { header1: 'cat', header2: 'dog', header3: 'fish', header4: 'snake' }
]