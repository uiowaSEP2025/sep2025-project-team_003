import { Component, ViewChild, AfterViewInit, Input, input, OnChanges, SimpleChanges } from '@angular/core';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { MatIconModule } from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { DeleteDialogComponentComponent } from '../delete-dialog-component/delete-dialog-component.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { StandardApiResponse } from '../../interfaces/standard-api-response.interface';
import { Observable } from 'rxjs';


@Component({
  selector: 'app-table-component',
  imports: [MatTableModule, MatPaginatorModule, MatInputModule, MatSelectModule, ReactiveFormsModule,MatIconModule,MatButtonModule],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit, OnChanges {
  @Input() fetchedData: any = null
  @Input({ required: true }) serviceRequest!: (data: any) => Observable<StandardApiResponse>

  constructor(private router: Router, public dialog: MatDialog, private snackBar: MatSnackBar) {}

  searchControl = new FormControl('')
  page: number | null = null 
  pageSize: number | null = null 
  headers = ['header1', 'header2', 'header3', 'header4']
  headersWithActions = [...this.headers, 'actions']
  searchHint = input<string>("Use me to search the data")
  queryParams: any;

  // TODO: figure out how to do edit and delete redirects when the backend is integrated
  editRedirect = input.required<string>()
  deleteEndpoint = input.required<string>()


  data = new MatTableDataSource(this.fetchedData ?? []);   
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

      
      redirectEdit(id: number) {
        this.queryParams = this.fetchedData.data[0]
        this.router.navigate([`${this.editRedirect()}/${id}`],{
          queryParams: this.queryParams
        });
      }

      openDeleteDialog(id: number, args: any) {
        const dialogRef = this.dialog.open(DeleteDialogComponentComponent, {
          width: '300px',
          data: { id }
        });

        setTimeout(() => {
          document.getElementById('modal')?.removeAttribute('aria-hidden');
        }, 10);
    
        dialogRef.afterClosed().subscribe(result => {
          if (result) {
            this.serviceRequest(args).subscribe({
              next: () => {
                this.snackBar.open(`Delete successfully`, '', {
                  duration: 3000
                });
                window.location.reload(); //reload for now, may have a better solution
              },
              error: (error) => {
                if (error.status === 401) {
                  this.snackBar.open(`There is something wrong when deleting`, '', {
                    duration: 3000
                  });
                }
              }
            });
          }
        });
      }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes["fetchedData"]?.currentValue || changes["dataSource"]) {
      this.fetchedData = changes["fetchedData"].currentValue;
      this.data = new MatTableDataSource(this.fetchedData.data ?? []);
      this.headers = Object.keys(this.fetchedData.data[0]);
      this.headersWithActions = [...this.headers, 'actions']
      this.ngAfterViewInit()
    }
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