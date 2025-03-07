import { Component, ViewChild, AfterViewInit, Input, input, OnChanges, SimpleChanges, OnInit } from '@angular/core';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';

import { MatDialog } from '@angular/material/dialog';
import { DeleteDialogComponentComponent } from '../delete-dialog-component/delete-dialog-component.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { StandardApiResponse } from '../../interfaces/standard-api-response.interface';
import { Observable, Subscription } from 'rxjs';
import { StringFormatter } from '../../utils/string-formatter';


@Component({
  selector: 'app-table-component',
  imports: [
    MatTableModule,
    MatPaginatorModule,
    MatInputModule,
    MatSelectModule,
    ReactiveFormsModule,
    MatIconModule,
    MatButtonModule
  ],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit, OnChanges {
  @Input() fetchedData: any = null
  @Input({ required: true }) deleteRequest!: (data: any) => Observable<StandardApiResponse>
  @Input({ required: true }) loadDataToTable!: (search: string, pageSize: number, offSet: number) => void
  @Input() hideValues: string[] = []; // Make this optional, and initialize it with an empty array if not provided.
  searchHint = input<string>("Use me to search the data")

  constructor(private router: Router, public dialog: MatDialog, private snackBar: MatSnackBar,) { }

  searchControl = new FormControl('')
  stringFormatter = new StringFormatter()
  private searchSubscription: Subscription | null = null
  private dataSubscription: Subscription | null = null
  page: number | null = null
  pageSize: number | null = null
  dataSize: number | null = null
  headers = ['header1', 'header2', 'header3', 'header4']
  headersWithActions = [...this.headers, 'Actions']


  editRedirect = input.required<string>()

  data = new MatTableDataSource(this.fetchedData ?? []);

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  ngAfterViewInit() {
    if (this.dataSubscription) {
      this.dataSubscription.unsubscribe();
    }

    if (this.searchSubscription) {
      this.searchSubscription.unsubscribe();  //Unsubscribe after any request make to prevent duplication of requests
    }

    this.searchSubscription = this.searchControl.valueChanges.pipe(
      debounceTime(0), // Wait for 300ms after the last change
      distinctUntilChanged() // Only emit if the value has changed
    )
      .subscribe((searchTerm) => {
        this.refetch(searchTerm ?? "")
      });


    this.dataSubscription = this.paginator.page.pipe(
      debounceTime(100), // Wait for 300ms after the last page change
      distinctUntilChanged((prev, curr) => prev.pageIndex === curr.pageIndex && prev.pageSize === curr.pageSize) // Only emit if the page or page size has changed
    ).subscribe((page) => {
      this.page = page.pageIndex;   
      this.pageSize = page.pageSize;
      this.refetch(this.searchControl.value ?? "");
    });
  }

  redirectEdit(id: number, args: any) {
    const queryParams = args
    this.router.navigate([`${this.editRedirect()}/${id}`], {
      queryParams: queryParams
    });
  }

  openDeleteDialog(args: any) {
    const dialogRef = this.dialog.open(DeleteDialogComponentComponent, {
      width: '300px',
      data: args
    });

    setTimeout(() => {
      document.getElementById('modal')?.removeAttribute('aria-hidden');
    }, 10);

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deleteRequest(args).subscribe({
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
    if (changes["fetchedData"]?.currentValue || changes["dataSource"] || changes["formControl"]) {
      this.fetchedData = changes["fetchedData"].currentValue;
      this.data = new MatTableDataSource(this.fetchedData.data ?? []);
      this.dataSize = this.fetchedData.totalCount

      if (this.fetchedData.data[0] !== undefined) {
        this.headers = Object.keys(this.fetchedData.data[0]);
        this.headers = this.headers.map(header => this.stringFormatter.formatSnakeToCamel(header))
        this.headersWithActions = [...this.headers, 'Actions'].filter((header) => {
          return !this.hideValues.includes(header)
        })
      }
    }
  }

  ngOnDestroy() {
    if (this.searchSubscription) {
      this.searchSubscription.unsubscribe();
    }

    if (this.dataSubscription) {
      this.dataSubscription.unsubscribe();
    }
  }

  refetch(textField: string) {
    this.loadDataToTable(textField, this.pageSize ?? 20, this.page ?? 0)
  }
}
