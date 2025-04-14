import { TestBed } from '@angular/core/testing';

import { ConfirmPasswordResetServiceService } from './confirm-password-reset.service';

describe('ConfirmPasswordResetServiceService', () => {
  let service: ConfirmPasswordResetServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ConfirmPasswordResetServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
