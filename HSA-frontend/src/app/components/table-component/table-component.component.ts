import { Component, ViewChild, AfterViewInit, Input, input, OnChanges, SimpleChanges, ChangeDetectorRef, OnDestroy, ElementRef } from '@angular/core';
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
import { OnInit } from '@angular/core';
import { InputFieldDictionary } from '../../interfaces/interface-helpers/inputField-row-helper.interface';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';

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
    ClickStopPropagationDirective,
    LoadingFallbackComponent
  ],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit, OnChanges, OnDestroy, OnInit {
  @Input() fetchedData: any = null
  @Input() deleteRequest!: (data: any) => Observable<StandardApiResponse>
  @Input({ required: true }) loadDataToTable!: (search: string, pageSize: number, offSet: number) => void
  @Input() hideValues: string[] = [];
  @Input() width: string = 'auto'
  @Input() checkbox: 'none' | 'single' | 'multiple' = 'none';
  @Input() unitUsedField: boolean = false;
  @Input() pricePerUnitField: boolean = false;
  @Input() checkedIds: number[] | null = null;
  @Input() materialInputFields: InputFieldDictionary[] = []
  @Input() setCheckedIds: ((checkedIds: number[]) => void) | null = null;
  @Input() setMaterialInputFields: ((inputFields: InputFieldDictionary[]) => void) | null = null;
  @Input() hideSearch: boolean = false
  @Input() clickableRows: boolean = false
  @Input() onRowClick: any = null // if clickable rows is enabled this the function that handles the click
  @Input() headers = ['header1', 'header2', 'header3', 'header4'] // headers to render before fetching the data
  // note: headers are decided based on backend json keys
  searchHint = input<string>("Use me to search the data")

  constructor(private router: Router, public dialog: MatDialog, private snackBar: MatSnackBar) {
  }

  searchControl = new FormControl('')
  stringFormatter = new StringFormatter()
  private searchSubscription: Subscription | null = null
  private dataSubscription: Subscription | null = null
  page: number | null = null
  pageSize: number | null = null
  dataSize: number | null = null
  checkedRowIndexes = new Set<number>();

  headersWithActions = [...this.headers, 'Actions']
  editRedirect = input.required<string>()
  isDataNotAvailable: boolean = false

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

    if (this.checkbox !== 'none') {
      if (!this.headersWithActions.includes('Checkbox')) {

        this.headersWithActions = ['Checkbox', ...this.headersWithActions]
      }
    }

    if (this.unitUsedField === true) {
      if (!this.headersWithActions.includes('Unit Used')) {
        this.headersWithActions = [...this.headersWithActions, 'Unit Used', 'Price Per Unit']
      }
    }

    if (this.fetchedData !== undefined) {
      if (this.fetchedData.length !== 0) {
        if (this.fetchedData.data !== undefined) {
          this.isDataNotAvailable = this.fetchedData.data.length === 0
        }
      }
    }
  }

  redirectEdit(id: number, args: any) {
    const queryParams = args
    console.log(queryParams)
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
      this.isDataNotAvailable = this.dataSize === 0 ? true : false

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
        }

        if (this.unitUsedField === true) {
          this.headersWithActions = [...this.headersWithActions, 'Unit Used', 'Price Per Unit']
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

  handleCheckedRowIndex(id: number) {
    if (this.checkedRowIndexes.has(id)) {
      this.checkedRowIndexes.delete(id);
      if (this.unitUsedField === true) {
        let currentUnitsUsedDict = this.materialInputFields.filter((item) => item.id !== id)
        this.setMaterialInputFields!(currentUnitsUsedDict)
      }
    } else {
      this.checkedRowIndexes.add(id);
    }
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

  handleUnitsUsedField(id: number, event: Event) {
    if (this.unitUsedField === true) {
      const parsedNumber = parseFloat((event.target as HTMLInputElement).value);
      const number = isNaN(parsedNumber) ? 0: parsedNumber
      let currentUnitsUsedDict = this.materialInputFields
      let specificEntry = currentUnitsUsedDict.find((item) => item.id === id)

      if (specificEntry) {
        specificEntry['unitsUsed'] = number
      }

      this.setMaterialInputFields!(currentUnitsUsedDict)
    }
  }

  handlePricePerUnitField(id: number, event: Event) {
    if (this.pricePerUnitField === true) {
      const parsedNumber = parseFloat((event.target as HTMLInputElement).value);
      const number = isNaN(parsedNumber) ? 0: parsedNumber
      let currentUnitsUsedDict = this.materialInputFields
      let specificEntry = currentUnitsUsedDict.find((item) => item.id === id)

      if (specificEntry) {
        specificEntry['pricePerUnit'] = number
      }

      this.setMaterialInputFields!(currentUnitsUsedDict)
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

  getUnitsUsedValue(id: number): number | string {
    const entry = this.materialInputFields.find(item => item.id === id);
    return entry?.['unitsUsed'] ?? '';
  }

  getPricePerUnitValue(id: number): number | string {
    const entry = this.materialInputFields.find(item => item.id === id);
    return entry?.['pricePerUnit'] ?? '';
  }
}
