import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

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

  login(data: LoginPostData): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }
}
