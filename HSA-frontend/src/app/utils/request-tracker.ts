import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class RequestTrackerService {
  private activeRequests = 0;
  private allRequestsCompleted$ = new Subject<void>();

  startRequest() {
    this.activeRequests++;
  }

  endRequest() {
    this.activeRequests--;
    if (this.activeRequests === 0) {
      this.allRequestsCompleted$.next();
    }
  }

  get completionNotifier() {
    return this.allRequestsCompleted$.asObservable();
  }
}
