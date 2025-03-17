import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateInvoicePageComponent } from './create-invoice-page.component';

describe('CreateInvoicePageComponent', () => {
  let component: CreateInvoicePageComponent;
  let fixture: ComponentFixture<CreateInvoicePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateInvoicePageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateInvoicePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should contain the correct elements', () => {
    const compiled = fixture.debugElement.nativeElement;
    const table = compiled.querySelector('table');
    expect(table).toBeTruthy()
    
  }) 
});
