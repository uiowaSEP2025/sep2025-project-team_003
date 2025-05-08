import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobDisplayTableComponent } from './job-display-table.component';

describe('JobDisplayTableComponent', () => {
  let component: JobDisplayTableComponent;
  let fixture: ComponentFixture<JobDisplayTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobDisplayTableComponent],
    })
    .compileComponents();

    fixture = TestBed.createComponent(JobDisplayTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
