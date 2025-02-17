import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditServicePageComponent } from './edit-service-page.component';

describe('EditServicePageComponent', () => {
  let component: EditServicePageComponent;
  let fixture: ComponentFixture<EditServicePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditServicePageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditServicePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
