import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { TableComponentComponent } from './table-component.component';
import { HarnessLoader } from '@angular/cdk/testing';
import {TestbedHarnessEnvironment} from '@angular/cdk/testing/testbed';
import {MatPaginatorHarness} from '@angular/material/paginator/testing';

describe('TableComponentComponent', () => {
  let component: TableComponentComponent;
  let fixture: ComponentFixture<TableComponentComponent>;
  let loader: HarnessLoader;


  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TableComponentComponent],
      providers: [provideAnimationsAsync()]
    })
      .compileComponents();

    fixture = TestBed.createComponent(TableComponentComponent);
    component = fixture.componentInstance;
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

  it('should render the search and select', () => {
    const compiled = fixture.debugElement.nativeElement;
    const search = compiled.querySelector('input')
    const select = compiled.querySelector('mat-select')
    expect(search).toBeTruthy()
    expect(select).toBeTruthy()
  })


  it('should change the page size class variable on page size change', async () => {
    const paginator = await loader.getHarness(MatPaginatorHarness);
    await paginator.setPageSize(10)
    expect(component.pageSize).toEqual(10)
  }) 

  it('should change the page offset class variable on page change', async () => {
    const paginator = await loader.getHarness(MatPaginatorHarness);
    await paginator.setPageSize(10)
    await paginator.goToNextPage();
    expect(component.page).toEqual(1)
  })

});
