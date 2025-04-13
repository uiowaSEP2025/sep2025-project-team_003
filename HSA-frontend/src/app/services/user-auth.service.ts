import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
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

  constructor(private http: HttpClient) {}

  login(data: LoginPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiLoginUrl, data);
  }

  logout() {
    return this.http.post<StandardApiResponse>(this.apiLogoutUrl, null);
  }

  createUser(data: CreateUserPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiUserCreateUrl, data);
  }

  public checkUserExist(data: LoginPostData) {
    return this.http.post<StandardApiResponse>(this.apiUserExistUrl, data)
  }
}
