import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { ReactiveFormsModule, FormControl, ValidatorFn, ValidationErrors,
  FormGroup, AbstractControl, FormGroupDirective, NgForm } from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

/** Error when invalid control is dirty, touched, or submitted. */
class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    return !!(control?.parent && control.parent.invalid && (control.parent.dirty || control.parent.touched));
  }
}

export const formValidator: ValidatorFn = (
  control: AbstractControl,
): ValidationErrors | null => {
  const searchText = control.get('searchControl')?.value;
  const select = control.get('selectControl')?.value;
  if (searchText && !select) {
    return {mustSelect: true}
  }
  if (!searchText && select) {
    return {mustSearch: true}
  }
  return null
};

// TODO: for data fetching, add a service: https://stackademic.com/blog/fetching-data-from-an-api-in-angular
@Component({
  selector: 'app-table-component',
  imports: [MatTableModule, MatPaginatorModule, MatInputModule, MatSelectModule, ReactiveFormsModule],
  templateUrl: './table-component.component.html',
  styleUrl: './table-component.component.scss'
})
export class TableComponentComponent implements AfterViewInit {
  queryGroup = new FormGroup({
    searchControl: new FormControl(''),
    selectControl: new FormControl('', )
  }, { validators: formValidator })

  page:number | null = null // null when unspecified
  pageSize:number | null = null // null when unspecified
  headers = ['header1', 'header2', 'header3', 'header4']
  data = new MatTableDataSource(rows)
  matcher = new MyErrorStateMatcher();
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  refetchData(searchTerm: string | null, searchHeader: string | null) {
    // TODO: fix it in service ticket, add a mock in the test to ensure that it only fetches when valid
    console.log(`Fetching data with search term: ${searchTerm}, header: ${searchHeader}
      pageSize: ${this.pageSize}, pageIndex: ${this.page}`);
  }

  ngAfterViewInit() {
    this.data.paginator = this.paginator;
    this.queryGroup.controls.searchControl.valueChanges
      .pipe(
        debounceTime(300), // Wait for 300ms after the last change
        distinctUntilChanged() // Only emit if the value has changed
      )
      .subscribe((searchTerm) => {
        if (this.queryGroup.valid) {this.refetchData(searchTerm,this.queryGroup.controls.selectControl.value);}
        
      });
    
    this.queryGroup.controls.selectControl.valueChanges
      .pipe(
        debounceTime(300), 
        distinctUntilChanged()
      )
      .subscribe(headerName => {
        if (this.queryGroup.valid) {this.refetchData(this.queryGroup.controls.searchControl.value,headerName);}
      });

      this.paginator.page.subscribe((page) => {
        this.page = page.pageIndex;
        this.pageSize = page.pageSize;
        if (this.queryGroup.valid) {this.refetchData(this.queryGroup.controls.searchControl.value,this.queryGroup.controls.selectControl.value);}
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