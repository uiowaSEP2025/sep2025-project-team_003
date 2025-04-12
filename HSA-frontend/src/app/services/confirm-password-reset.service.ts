import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ConfirmPasswordResetServiceService {
  private url = `${environment.apiUrl}/api/password_reset/confirm/`;

  constructor(private http: HttpClient) { }

  confirmPasswordReset(password: string, token: string) {
    const formdata = new FormData()
    formdata.append("password", password)
    formdata.append("token", token)

    this.http.post(this.url, formdata)

  }
}
