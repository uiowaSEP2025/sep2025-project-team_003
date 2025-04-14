import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';

interface LoginPostData {
  username: string | null
  password: string | null
}

interface CreateUserPostData {
  firstName: string | null
  lastName: string | null
  email: string | null
  username: string | null
  password: string | null
}

@Injectable({
  providedIn: 'root'
})
export class UserAuthService {
  private apiLoginUrl = `${environment.apiUrl}/api/login`;
  private apiLogoutUrl = `${environment.apiUrl}/api/logout`;
  private apiUserCreateUrl = `${environment.apiUrl}/api/create/user`;
  private apiUserExistUrl = `${environment.apiUrl}/api/userexist`;

  private _isLoggedIn$ = new BehaviorSubject<boolean>(false);
  public isLoggedIn$ = this._isLoggedIn$.asObservable();

  constructor(private http: HttpClient) {}

  login(data: LoginPostData):Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiLoginUrl, data).pipe(
      tap(response => {
        // You can check response.success or a similar field
        if (response) {
          this._isLoggedIn$.next(true);
        }
      })
    );
  }

  logout():Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiLogoutUrl, null).pipe(
      tap(() => {
        this._isLoggedIn$.next(false);
      })
    );
  }

  createUser(data: CreateUserPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiUserCreateUrl, data);
  }

  public checkUserExist(data: LoginPostData) {
    return this.http.post<StandardApiResponse>(this.apiUserExistUrl, data)
  }

  public setLoginStatus(status: boolean): void {
    this._isLoggedIn$.next(status);
  }
}
