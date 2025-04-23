import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewRequestComponentComponent } from './view-request-component.component';

describe('ViewRequestComponentComponent', () => {
  let component: ViewRequestComponentComponent;
  let fixture: ComponentFixture<ViewRequestComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewRequestComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewRequestComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
