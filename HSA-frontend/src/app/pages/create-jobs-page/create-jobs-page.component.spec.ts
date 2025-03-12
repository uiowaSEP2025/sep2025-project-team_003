import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateJobsPageComponent } from './create-jobs-page.component';

describe('CreateJobsPageComponent', () => {
  let component: CreateJobsPageComponent;
  let fixture: ComponentFixture<CreateJobsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateJobsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateJobsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
