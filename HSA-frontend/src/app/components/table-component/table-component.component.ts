import { Component, ViewChild, AfterViewInit, input } from '@angular/core';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { MatIconModule } from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { Router } from '@angular/router';
import 

// TODO: for data fetching, add a service: https://stackademic.com/blog/fetching-data-from-an-api-in-angular
@Component({
  selector: 'app-table-component',
  imports: [MatTableModule, MatPaginatorModule, MatInputModule, MatSelectModule, ReactiveFormsModule,MatIconModule,MatButtonModule],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit {

  constructor(private router: Router) {}

  searchControl = new FormControl('')
  page:number | null = null // null when unspecified
  pageSize:number | null = null // null when unspecified
  headers = ['header1', 'header2', 'header3', 'header4']
  headersWithActions = [...this.headers, 'actions']
  searchHint = input<string>("Use me to search the data")
  // TODO: figure out how to do edit and delete redirects when the backend is integrated
  editRedirect = input.required<string>() // the URL to edit the component
  deleteEndpoint = input.required<string>()
  data = new MatTableDataSource(this.dataInput().data);   
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  refetchData(searchTerm: string | null) {
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

      this.paginator.page.subscribe((page) => {
        this.page = page.pageIndex;
        this.pageSize = page.pageSize;
        this.refetchData(this.searchControl.value);
      })}

      redirectEdit() {
        //TODO: find out how to pass the query params properly on backend integrate
        this.router.navigate([`${this.editRedirect()}/1`],{
          queryParams: { email: 'aguo2@uiowa.edu', fname: 'alex', lname: 'guo', phoneNo: '1111111111' }
        });
        
      }
}
