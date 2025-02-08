import { Component, ViewChild, AfterViewInit, input } from '@angular/core';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { ReactiveFormsModule } from '@angular/forms';

// TODO: for data fetching, add a service: https://stackademic.com/blog/fetching-data-from-an-api-in-angular
@Component({
  selector: 'app-table-component',
  imports: [MatTableModule, MatPaginatorModule, MatInputModule, MatSelectModule, ReactiveFormsModule],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit {
  searchControl = new FormControl('');
  selectControl = new FormControl('');
  page:number | null = null // null when unspecified
  pageSize:number | null = null // null when unspecified
  headers = ['header1', 'header2', 'header3', 'header4']
  data = new MatTableDataSource(rows)
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  refetchData(searchTerm: string | null, searchHeader: string | null) {
    // TODO: fix it in service ticket
    console.log(`Fetching data with search term: ${searchTerm}, header: ${searchHeader}
      pageSize: ${this.pageSize}, pageIndex: ${this.page}`);
  }

  ngAfterViewInit() {
    this.data.paginator = this.paginator;
    this.searchControl.valueChanges
      .pipe(
        debounceTime(300), // Wait for 300ms after the last change
        distinctUntilChanged() // Only emit if the value has changed
      )
      .subscribe(searchTerm => {
        this.refetchData(searchTerm,this.selectControl.value);
      });
    
    this.selectControl.valueChanges
      .pipe(
        debounceTime(300), 
        distinctUntilChanged()
      )
      .subscribe(headerName => {
        this.refetchData(this.searchControl.value,headerName);
      });

      this.paginator.page.subscribe((page) => {
        this.page = page.pageIndex;
        this.pageSize = page.pageSize;
        this.refetchData(this.searchControl.value,this.selectControl.value);
      })

      

  }
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