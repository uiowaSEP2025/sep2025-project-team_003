import { TestBed } from '@angular/core/testing';

import { RequestPasswordResetService } from './request-password-reset.service';

describe('RequestPasswordResetService', () => {
  let service: RequestPasswordResetService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RequestPasswordResetService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
