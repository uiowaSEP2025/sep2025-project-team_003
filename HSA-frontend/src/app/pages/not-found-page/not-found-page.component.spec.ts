import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NotFoundPageComponent } from './not-found-page.component';
import {provideRouter} from '@angular/router';

describe('NotFoundPageComponent', () => {
  let component: NotFoundPageComponent;
  let fixture: ComponentFixture<NotFoundPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NotFoundPageComponent],
      providers: [provideRouter([])]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NotFoundPageComponent);
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

    expect(header.textContent).toContain('404 - Page Not Found')
    expect(txt.textContent).toContain('Oops! It seems like the resource you\'re trying to access or modify does not exist.')
    expect(button).toBeTruthy()

  })
});
