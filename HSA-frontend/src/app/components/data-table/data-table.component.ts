import {Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {
  MatCell,
  MatCellDef,
  MatColumnDef,
  MatHeaderCell,
  MatHeaderCellDef, MatHeaderRow, MatHeaderRowDef, MatRow, MatRowDef,
  MatTable,
  MatTableDataSource
} from '@angular/material/table';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import {DataService} from '../../services/data.service';
import {MatInput} from '@angular/material/input';
import {FormsModule} from '@angular/forms';
import {MatFormField} from '@angular/material/form-field';
import {MatIcon} from '@angular/material/icon';
import {MatIconButton} from '@angular/material/button';
import {finalize} from 'rxjs';
import {ConfirmationDialogComponent} from '../confirmation-dialog/confirmation-dialog.component';
import {MatDialog} from '@angular/material/dialog';

interface FieldInfo {
  name: string;
  verbose_name: string;
  type: string;
}

@Component({
  selector: 'app-data-table',
  imports: [
    MatPaginator,
    MatTable,
    MatFormField,
    MatInput,
    FormsModule,
    MatColumnDef,
    MatHeaderCell,
    MatHeaderCellDef,
    MatCellDef,
    MatCell,
    MatHeaderRow,
    MatHeaderRowDef,
    MatRow,
    MatRowDef,
    MatIcon,
    MatIconButton,
  ],
  templateUrl: './data-table.component.html',
  styleUrl: './data-table.component.scss'
})
export class DataTableComponent implements OnInit {

  private _isLoading = false;
  set isLoading(value: boolean) {
    this._isLoading = value;
    this.loadingChange.emit(value)
  }
  get isLoading(): boolean {
    return this._isLoading;
  }

  @Input() lookupTable = ''
  dataSource = new MatTableDataSource<any>([]);
  displayedColumns: string[] = [];
  @Input() excludeColumns: string[] = [];
  fields: FieldInfo[] = [];
  totalItems = 0;
  pageSize = 10;
  currentPage = 0;
  searchTerm = '';
  finalColumns: string[] = [];

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private dataService: DataService,
              private dialog: MatDialog) {}
  // Add actions to displayed columns

  displayedColumnsWithActions: string[] = [];
  @Output() loadingChange = new EventEmitter<boolean>();
  @Output() edit = new EventEmitter<any>();
  @Output() delete = new EventEmitter<any>();
  ngOnInit() {
    this.isLoading = true;
    this.loadData();
  }

  loadData() {
    this.dataService.getData(
      this.lookupTable,
      this.currentPage + 1,
      this.pageSize,
      this.searchTerm
    ).pipe(
      finalize(() => {
        this.isLoading = false;
      })
    ).subscribe(response => {
      this.dataSource.data = response.data;
      this.totalItems = response.total_items;
      this.fields = response.fields;

      // Set displayed columns based on fields
      this.displayedColumns = this.fields.map(field => field.name).filter(columnName => !this.excludeColumns.includes(columnName));
      this.displayedColumnsWithActions = [...this.displayedColumns, 'actions']
    });
  }

  getColumnHeader(columnName: string): string {
    const field = this.fields.find(f => f.name === columnName);
    return field ? field.verbose_name : columnName;
  }

  formatCellValue(value: any, columnName: string): string {
    const field = this.fields.find(f => f.name === columnName);
    if (!field) return value;

    switch (field.type) {
      case 'DateTimeField':
        return new Date(value).toLocaleString();
      case 'DateField':
        return new Date(value).toLocaleDateString();
      case 'BooleanField':
        return value ? 'Yes' : 'No';
      case 'DecimalField':
      case 'FloatField':
        return typeof value === 'number' ? value.toFixed(2) : value;
      default:
        return value;
    }
  }

  onPageChange(event: PageEvent) {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadData();
  }

  onSearch(term: string) {
    this.searchTerm = term;
    this.currentPage = 0;
    this.loadData();
  }

  onEdit(row: any) {
    if (!this.isLoading) {
    this.edit.emit(row);
    }
  }

  onDelete(row: any) {
    if (this.isLoading) return;
    const dialogRef = this.dialog.open(ConfirmationDialogComponent), {
      data: {item: row}
    });
    this.delete.emit(row.id);
  }
}
