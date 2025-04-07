import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobsHelperComponent } from './jobs-helper.component';

describe('JobsHelperComponent', () => {
  let component: JobsHelperComponent;
  let fixture: ComponentFixture<JobsHelperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobsHelperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(JobsHelperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
