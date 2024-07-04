import { TestBed } from '@angular/core/testing';

import { MissionDataShareService } from './mission-data-share.service';

describe('MissionDataShareService', () => {
  let service: MissionDataShareService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MissionDataShareService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
