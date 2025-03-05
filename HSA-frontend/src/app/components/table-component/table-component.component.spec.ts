import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { TableComponentComponent } from './table-component.component';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { MatPaginatorHarness } from '@angular/material/paginator/testing';
import { MatCheckboxHarness } from '@angular/material/checkbox/testing';
import { SimpleChanges, SimpleChange } from '@angular/core';


describe('TableComponentComponent', () => {
  let component: TableComponentComponent;
  let fixture: ComponentFixture<TableComponentComponent>;
  let loader: HarnessLoader;
  let mockLoadData: (search: string, pageSize: number, offSet: number) => void;
  let deleteFNMock: any
  let refetchMock: any
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

  it('should render the edit and delete icons in the row', () => {
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

  it('should refetch when the search is changed', async () => {
    const compiled = fixture.debugElement.nativeElement;
    refetchMock = jasmine.createSpy('refetch');
    component.refetch = refetchMock
    const search = compiled.querySelector('input')
    search.value = "search param"
    search.dispatchEvent(new Event('input'));
    fixture.detectChanges()
    await (new Promise(resolve => setTimeout(resolve, 1000))) // this has to be here or it fails :(
    expect(component.refetch).toHaveBeenCalled();
  })

  it('should refetch when the paginator is changed', async () => {
    const paginator = await loader.getHarness(MatPaginatorHarness);
    component.dataSize = 100
    await paginator.setPageSize(20)
    await paginator.goToNextPage();
    expect(mockLoadData).toHaveBeenCalled();
  })

  it('should hide the row properly', () => {
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
    component.hideValues = ["Name"]
    component.ngOnChanges(changes);
    fixture.detectChanges(); // Trigger change detection
    const row = compiled.querySelector('table').querySelectorAll('tr')[1]
    const rowText = row.textContent

    expect(rowText).not.toContain("Name");
    expect(rowText).not.toContain("name");
  })

  it('should render the header data', async () => {
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
    const row = compiled.querySelector('table').querySelectorAll('tr')[0]
    const rowText = row.textContent
    await (new Promise(resolve => setTimeout(resolve, 2000)))
    expect(rowText).toContain("Name");
    expect(rowText).toContain("Id");
    expect(rowText).toContain("Email");
  })

  it('should render the header data', async () => {
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
    const rowText = row.textContent
    await (new Promise(resolve => setTimeout(resolve, 2000)))
    expect(rowText).toContain("1");
    expect(rowText).toContain("John Doe");
    expect(rowText).toContain("john@example.com");
  })

  describe('checkbox tests', () => {
    let setCheckedIds: any
    let checkedIds: number[] = []

    describe('single select', () => {
      beforeEach(() => {
        // Have to manually trigger the event or it won't work :()
        const mockData = {
          data: [
            { id: 1, name: 'John Doe', email: 'john@example.com' },
            { id: 2, name: 'Jane Doe', email: 'jane@example.com' }
          ],
          totalCount: 100
        };
        component.checkbox = "single"
        component.checkedIds = checkedIds
        const changes: SimpleChanges = {
          fetchedData: new SimpleChange(null, mockData, true) // true indicates it's the first change
        };
        component.ngOnChanges(changes);
        fixture.detectChanges(); // Trigger change detection

      })

      it('should successfully select a single row', async () => {
        setCheckedIds = jasmine.createSpy().and.callFake((arg) => {
          checkedIds = [...arg]
        });

        component.setCheckedIds = setCheckedIds
        const checkboxes = await loader.getAllHarnesses(MatCheckboxHarness);
        const c0 = checkboxes[0]
        await c0.toggle()
        fixture.detectChanges()

        expect(setCheckedIds).toHaveBeenCalledWith([1])
        expect(await c0.isChecked()).toBe(true)
      })

      it('should only allow one row selected', async () => {
        setCheckedIds = jasmine.createSpy().and.callFake((arg) => {
          checkedIds = [...arg]
          fixture.detectChanges(); // Trigger update in the component

          console.log('setter', checkedIds, arg)
        });
        component.setCheckedIds = setCheckedIds
        const compiled = fixture.debugElement.nativeElement;
        const checkboxes = await loader.getAllHarnesses(MatCheckboxHarness);
        const c0 = checkboxes[0]
        await c0.toggle()
        fixture.detectChanges()
        expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([1])) // we make sure that checkedIds has the right value before assigning it
        component.checkedIds = checkedIds // you have to do this or it won't work.
        expect(setCheckedIds).toHaveBeenCalledWith([1])
        expect(await c0.isChecked()).toBe(true)
        await fixture.whenStable()
        const c1 = checkboxes[1]
        await c1.toggle()
        fixture.detectChanges()
        expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([2])) // we make sure that checkedIds has the right value before assigning it
        component.checkedIds = checkedIds // you have to do this or it won't work.
        await fixture.whenStable()
        expect(setCheckedIds).toHaveBeenCalledWith([2])
        expect(await c1.isChecked()).toBe(true)
        expect(await c0.isChecked()).toBe(false)
      })

      it('should successfully unselect', async () => {
        setCheckedIds = jasmine.createSpy().and.callFake((arg) => {
          checkedIds = [...arg]
        });

        component.setCheckedIds = setCheckedIds
        const checkboxes = await loader.getAllHarnesses(MatCheckboxHarness);
        const c0 = checkboxes[0]
        await c0.toggle()
        fixture.detectChanges()
        
        expect(setCheckedIds).toHaveBeenCalledWith([1])
        expect(await c0.isChecked()).toBe(true)

        expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([1]))
        component.checkedIds = checkedIds // you have to do this or it won't work.

        await c0.toggle()
        fixture.detectChanges()
        expect(setCheckedIds).toHaveBeenCalledWith([1])
        expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([]))
        expect(await c0.isChecked()).toBe(false)
      })

      describe('multiple select', () => {

        beforeEach(() => {
          // Have to manually trigger the event or it won't work :()
          const mockData = {
            data: [
              { id: 1, name: 'John Doe', email: 'john@example.com' },
              { id: 2, name: 'Jane Doe', email: 'jane@example.com' }
            ],
            totalCount: 100
          };
          component.checkbox = "multiple"
          component.checkedIds = checkedIds
          const changes: SimpleChanges = {
            fetchedData: new SimpleChange(null, mockData, true) // true indicates it's the first change
          };
          component.ngOnChanges(changes);
          fixture.detectChanges(); // Trigger change detection
  
        })

        it('should successfully select multiple rows', async () => {
          setCheckedIds = jasmine.createSpy().and.callFake((arg) => {
            checkedIds = [...arg]
          });
  
          component.setCheckedIds = setCheckedIds
          const checkboxes = await loader.getAllHarnesses(MatCheckboxHarness);
          const c0 = checkboxes[0]
          await c0.toggle()
          fixture.detectChanges()
          
          expect(setCheckedIds).toHaveBeenCalledWith([1])
          expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([1]))

          component.checkedIds = checkedIds
          expect(await c0.isChecked()).toBe(true)

          const c1 = checkboxes[1]
          await c1.toggle()
          fixture.detectChanges()
          
          expect(setCheckedIds).toHaveBeenCalledWith([1,2])
          expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([1,2]))
          component.checkedIds = checkedIds
          expect(await c0.isChecked()).toBe(true)
          expect(await c1.isChecked()).toBe(true)
        })


        fit('should successfully unselect', async() => {
          setCheckedIds = jasmine.createSpy().and.callFake((arg) => {
            checkedIds = [...arg]
          });
  
          component.setCheckedIds = setCheckedIds
          const checkboxes = await loader.getAllHarnesses(MatCheckboxHarness);
          const c0 = checkboxes[0]
          await c0.toggle()
          fixture.detectChanges()
          
          expect(setCheckedIds).toHaveBeenCalledWith([1])
          expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([1]))

          component.checkedIds = checkedIds
          expect(await c0.isChecked()).toBe(true)

          const c1 = checkboxes[1]
          await c1.toggle()
          fixture.detectChanges()
          
          expect(setCheckedIds).toHaveBeenCalledWith([1,2])
          expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([1,2]))
          component.checkedIds = checkedIds
          expect(await c0.isChecked()).toBe(true)
          expect(await c1.isChecked()).toBe(true)

          await c0.toggle()
          fixture.detectChanges()
          
          expect(setCheckedIds).toHaveBeenCalledWith([1])
          expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([2]))
          component.checkedIds = checkedIds
          expect(await c0.isChecked()).toBe(false)
          expect(await c1.isChecked()).toBe(true)

          await c1.toggle()
          fixture.detectChanges()
          
          expect(setCheckedIds).toHaveBeenCalledWith([2])
          expect(JSON.stringify(checkedIds)).toEqual(JSON.stringify([]))
          expect(await c0.isChecked()).toBe(false)
          expect(await c1.isChecked()).toBe(false)
        })})})

    afterEach(() => {
      setCheckedIds.calls.reset()
    })

  })
});
