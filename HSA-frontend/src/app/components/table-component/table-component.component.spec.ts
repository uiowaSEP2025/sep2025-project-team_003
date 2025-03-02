import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { TableComponentComponent } from './table-component.component';
import { HarnessLoader } from '@angular/cdk/testing';
import {TestbedHarnessEnvironment} from '@angular/cdk/testing/testbed';
import {MatPaginatorHarness} from '@angular/material/paginator/testing';
import { SimpleChanges, SimpleChange } from '@angular/core';


interface UserData {
  id: number;
  name: string;
  email: string;
}

describe('TableComponentComponent', () => {
  let component: TableComponentComponent;
  let fixture: ComponentFixture<TableComponentComponent>;
  let loader: HarnessLoader;
  let mockLoadData: (search: string, pageSize: number, offSet: number) => void;
  let deleteFNMock: any
  beforeEach(async () => {
    const mockData = {
      data: [
        { id: 1, name: 'John Doe', email: 'john@example.com' },
        { id: 2, name: 'Jane Doe', email: 'jane@example.com' }
      ],
      totalCount: 100
    };

    mockLoadData = jasmine.createSpy('loadData');
    deleteFNMock = jasmine.createSpy('delete');

    await TestBed.configureTestingModule({
      imports: [TableComponentComponent],
      providers: [provideAnimationsAsync()]
    })
      .compileComponents();

    fixture = TestBed.createComponent(TableComponentComponent);
    component = fixture.componentInstance;
    component.fetchedData = mockData;
    component.loadDataToTable = mockLoadData
    component.deleteRequest = deleteFNMock
    loader = TestbedHarnessEnvironment.loader(fixture);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the paginator', () => {
    const compiled = fixture.debugElement.nativeElement;
    const paginator = compiled.querySelector('mat-paginator')
    expect(paginator).toBeTruthy()
  })

  it('should render the search bar', () => {
    const compiled = fixture.debugElement.nativeElement;
    const search = compiled.querySelector('input')
    expect(search).toBeTruthy()
  })

  it('should change the page size class variable on page size change', async () => {
    const paginator = await loader.getHarness(MatPaginatorHarness);
    await paginator.setPageSize(20)
    expect(component.pageSize).toEqual(20)
  }) 

  it('should render the edit and delete icons in the row',  () => {
    const compiled = fixture.debugElement.nativeElement;
    // Have to manually trigger the event or it won't work :()
    const mockData = {
      data: [
        { id: 1, name: 'John Doe', email: 'john@example.com' },
        { id: 2, name: 'Jane Doe', email: 'jane@example.com' }
      ],
      totalCount: 100
    };
    const changes: SimpleChanges = {
      fetchedData: new SimpleChange(null, mockData, true) // true indicates it's the first change
    };

    component.ngOnChanges(changes);
    fixture.detectChanges(); // Trigger change detection
    const row = compiled.querySelector('table').querySelectorAll('tr')[1]

    const icons = row.querySelectorAll('mat-icon')
    expect(icons.length).toEqual(2)
    expect(icons[0].textContent).toEqual('edit')
    expect(icons[1].textContent).toEqual('delete')
  })

  it('should change the page offset class variable on page change', async () => {
    const paginator = await loader.getHarness(MatPaginatorHarness);
    component.dataSize = 100
    await paginator.setPageSize(20)
    await paginator.goToNextPage();
    expect(component.page).toEqual(1)
  })

  it('should render the search hint text', () => {
    const compiled = fixture.debugElement.nativeElement;
    const hint = compiled.querySelector('mat-hint')
    expect(hint.textContent).toEqual('Use me to search the data')
  })
});
