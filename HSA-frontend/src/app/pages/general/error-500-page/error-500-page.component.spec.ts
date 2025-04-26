import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Error500PageComponent } from './error-500-page.component';

describe('Error500PageComponent', () => {
  let component: Error500PageComponent;
  let fixture: ComponentFixture<Error500PageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Error500PageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Error500PageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render correctly', () => {
    const compiled = fixture.debugElement.nativeElement;
    const header = compiled.querySelector('mat-card-header')
    const txt = compiled.querySelector('mat-card-content')
    const button = compiled.querySelector('button')

    expect(header.textContent).toContain('500 - Server Error')
    expect(txt.textContent).toContain('Oops! Something went wrong while processing your request')
    expect(button).toBeTruthy()

  })
});
