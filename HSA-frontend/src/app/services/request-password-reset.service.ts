import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RequestPasswordResetService {
  private url = `${environment.apiUrl}/api/password_reset/`;

  constructor(private http: HttpClient) { }

  requestPasswordReset(email: string) {
    // this is always 200
    const formdata = new FormData()
    formdata.append('email', email)

    return this.http.post(this.url, formdata)

  }

}
