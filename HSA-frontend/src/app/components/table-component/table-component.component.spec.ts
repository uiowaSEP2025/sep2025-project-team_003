import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { TableComponentComponent } from './table-component.component';
import {MatSelectHarness} from '@angular/material/select/testing';
import { HarnessLoader } from '@angular/cdk/testing';
import {TestbedHarnessEnvironment} from '@angular/cdk/testing/testbed';


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

  it('should be invalid when only search has value', () => {
    const compiled = fixture.debugElement.nativeElement;
    const search = compiled.querySelector('input')
    search.value = 'testing'

    search.dispatchEvent(new Event('input'));
    fixture.detectChanges(); 

    const errorElements:Element[] = Array.from(compiled.querySelectorAll('mat-error'))
    expect(errorElements.length).toEqual(1)
    expect(errorElements[0].textContent).toEqual('Please select a search header')    
  })

  it('should be invalid when only select has value', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const select = await loader.getHarness(MatSelectHarness);
    await select.open();

    const options = await select.getOptions();
    await options[1].click();
    fixture.detectChanges(); 
    const errorElements:Element[] = Array.from(compiled.querySelectorAll('mat-error'))
    expect(errorElements.length).toEqual(1)
    expect(errorElements[0].textContent).toEqual('Please enter a search term')    
  })

  it('should not call the refetch function when invalid', async () => {
    const refetchSpy = spyOn(component, 'refetchData')
    const select = await loader.getHarness(MatSelectHarness);
    await select.open();

    const options = await select.getOptions();
    await options[1].click();
    fixture.detectChanges(); 
    expect(refetchSpy).toHaveBeenCalledTimes(0)
  })

  it('should not call the refetch function when valid', async () => {
    const compiled = fixture.debugElement.nativeElement;
    const refetchSpy = spyOn(component, 'refetchData')
    
    const select = await loader.getHarness(MatSelectHarness);
    await select.open();
    const options = await select.getOptions();
    await options[1].click();
    fixture.detectChanges(); 
    
    const search = compiled.querySelector('input')
    search.value = 'testing'
    search.dispatchEvent(new Event('input'));
    fixture.detectChanges(); 
    await new Promise(resolve => setTimeout(resolve, 1000)) // this must be here or it fails.
    //this gives the unit test a second to run the form validator and call the refetch function

    expect(component.queryGroup.valid).toBeTrue();
    expect(refetchSpy).toHaveBeenCalledTimes(1)
  })

});
