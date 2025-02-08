import { Component,ViewChild,AfterViewInit,input } from '@angular/core';
import { MatTableModule,MatTableDataSource } from '@angular/material/table';
import { MatPaginator,MatPaginatorModule} from '@angular/material/paginator';
import {MatInputModule} from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

// TODO: for data fetching, add a service: https://stackademic.com/blog/fetching-data-from-an-api-in-angular
@Component({
  selector: 'app-table-component',
  imports: [MatTableModule, MatPaginatorModule, MatInputModule, MatSelectModule],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit {
  headers = ['header1','header2','header3','header4']
  data = new MatTableDataSource(rows) 
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  searchField = input(0);
  ngAfterViewInit() {
    this.data.paginator = this.paginator;
  }
}
 
const rows = [
  {header1: 'cat',header2: 'dog', header3: 'fish', header4: 'snake'},
  {header1: 'cat',header2: 'dog', header3: 'fish', header4: 'snake'},
  {header1: 'cat',header2: 'dog', header3: 'fish', header4: 'snake'},
  {header1: 'cat',header2: 'dog', header3: 'fish', header4: 'snake'},
  {header1: 'cat',header2: 'dog', header3: 'fish', header4: 'snake'}
]