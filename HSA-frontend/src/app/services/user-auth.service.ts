import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { StandardApiResponse } from '../interfaces/api-responses/standard-api-response.interface';

interface LoginPostData {
  username: string | null
  password: string | null
}


@Injectable({
  providedIn: 'root'
})
export class UserAuthService {
  private apiUrl = `${environment.apiUrl}/api/login`; // Example API

  constructor(private http: HttpClient) {}

  login(data: LoginPostData): Observable<StandardApiResponse> {
    return this.http.post<StandardApiResponse>(this.apiUrl, data);
  }
}
