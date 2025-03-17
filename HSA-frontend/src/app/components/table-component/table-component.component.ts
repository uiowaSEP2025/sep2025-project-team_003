import { Component, ViewChild, AfterViewInit, Input, input, OnChanges, SimpleChanges, ChangeDetectorRef, OnDestroy } from '@angular/core';
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
import { StandardApiResponse } from '../../interfaces/api-responses/standard-api-response.interface';
import { Observable, Subscription } from 'rxjs';
import { StringFormatter } from '../../utils/string-formatter';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { ClickStopPropagationDirective } from '../../utils/click-event-propogation-stopper';
import { ErrorHandlerService } from '../../services/error.handler.service';
import { OnInit } from '@angular/core';

@Component({
  selector: 'app-table-component',
  imports: [
    MatTableModule,
    MatPaginatorModule,
    MatInputModule,
    MatSelectModule,
    ReactiveFormsModule,
    MatIconModule,
    MatButtonModule,
    MatCheckboxModule,
    FormsModule,
    ClickStopPropagationDirective
  ],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit, OnChanges, OnDestroy, OnInit {
  @Input() fetchedData: any = null
  @Input() deleteRequest!: (data: any) => Observable<StandardApiResponse>
  @Input({ required: true }) loadDataToTable!: (search: string, pageSize: number, offSet: number) => void
  @Input() hideValues: string[] = [];
  @Input() checkbox: 'none' | 'single' | 'multiple' = 'none';
  @Input() checkedIds: number[] | null = null;
  @Input() setCheckedIds: ((checkedIds: number[]) => void) | null = null;
  @Input() hideSearch: boolean = false
  @Input() clickableRows: boolean = false
  @Input() onRowClick: any = null // if clickable rows is enabled this the function that handles the click
  @Input() headers = ['header1', 'header2', 'header3', 'header4'] // headers to render before fetching the data
  // note: headers are decided based on backend json keys
  searchHint = input<string>("Use me to search the data")

  constructor(private router: Router, public dialog: MatDialog, private snackBar: MatSnackBar, private errorHandler: ErrorHandlerService) {
  }

  searchControl = new FormControl('')
  stringFormatter = new StringFormatter()
  private searchSubscription: Subscription | null = null
  private dataSubscription: Subscription | null = null
  page: number | null = null
  pageSize: number | null = null
  dataSize: number | null = null
  
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

  ngOnInit(): void {
    this.headersWithActions = [...this.headers, 'Actions'].filter((header) => {
      return !this.hideValues.includes(header)
    }) // this has to be here to allow default headers change. On init is ran
    // when inputs are recieved
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
            this.snackBar.open(`Deleted successfully`, '', {
              duration: 3000
            });
            window.location.reload(); //reload for now, may have a better solution
          },
          error: (error) => {
            this.errorHandler.handleError(error)
          }
        });
      }
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    // this has to be here to change the headers, and does not affect how the headers are set based on the data
    if (changes["fetchedData"]?.currentValue || changes["dataSource"] || changes["formControl"]) {
      this.fetchedData = changes["fetchedData"].currentValue;
      this.data = new MatTableDataSource(this.fetchedData.data ?? []);
      this.dataSize = this.fetchedData.totalCount
      if (this.fetchedData.data && this.fetchedData.data[0] !== undefined) {
        this.headers = Object.keys(this.fetchedData.data[0]);
        this.headers = this.headers.map(header => this.stringFormatter.formatSnakeToCamel(header))
        if (this.checkbox === "none") {
          this.headersWithActions = [...this.headers, 'Actions'].filter((header) => {
            return !this.hideValues.includes(header)
          })
        }
        else {
          this.headersWithActions = ['Checkbox', ...this.headers].filter((header) => {
            return !this.hideValues.includes(header)
          })
          console.log(this.headersWithActions)
        }
      }
    }
  }

  rowClick(element: any) {
    if (!this.clickableRows) {
      return;
    }
    this.onRowClick(element)
  }

  handleCheckBoxClick(id: number) {
    if (this.checkbox === "single") {
      if (this.checkedIds?.includes(id)) {

        this.setCheckedIds!([])
        return
      }
      this.setCheckedIds!([id])
    }
    else if (this.checkbox === "multiple") {
      let ids = this.checkedIds
      if (ids?.includes(id)) {
        ids = ids.filter(element => element !== id);
        this.setCheckedIds!(ids!)
        return
      }
      ids?.push(id)
      this.setCheckedIds!(ids!)
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

  shouldCheckCheckbox(id: number): boolean {
    return this.checkedIds!.includes(id)
  }
}