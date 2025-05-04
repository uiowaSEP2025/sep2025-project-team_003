import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuoteSignComponent } from './quote-sign.component';

describe('QuoteSignComponent', () => {
  let component: QuoteSignComponent;
  let fixture: ComponentFixture<QuoteSignComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QuoteSignComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuoteSignComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
