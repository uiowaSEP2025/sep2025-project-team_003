import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateInvoicePageComponent } from './create-invoice-page.component';

fdescribe('CreateInvoicePageComponent', () => {
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

  it('should display error when no customer is selected', () => {})

  it('should display date picker when status is not created', () => {})

  it('should call validate on the view child', () => {})

  it('should show error when no quotes are selected', () => {})

  it('should call the endpoint when everything is valid', () => {})

});
