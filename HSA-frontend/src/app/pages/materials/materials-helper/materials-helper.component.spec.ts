import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MaterialsHelperComponent } from './materials-helper.component';

describe('MaterialsHelperComponent', () => {
  let component: MaterialsHelperComponent;
  let fixture: ComponentFixture<MaterialsHelperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MaterialsHelperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MaterialsHelperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
