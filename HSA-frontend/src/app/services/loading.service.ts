import {BehaviorSubject, finalize, Observable} from 'rxjs';
import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoadingService {
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  setLoading(loading: boolean) {
    this.loadingSubject.next(loading);
  }

  withLoading<T>(observable: Observable<T>): Observable<T> {
    return new Observable<T>(subscriber => {
      this.setLoading(true);

      return observable.pipe(
        finalize(() => this.setLoading(false))
      ).subscribe(subscriber);
    });
  }
}
