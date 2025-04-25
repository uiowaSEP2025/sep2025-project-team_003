import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';


interface ResetConfirmation404Response {
  detail: string
}

interface ResetConfirmationValidResponse {
  status: string
}

type ResetConfirmationResponse = ResetConfirmation404Response | ResetConfirmationValidResponse


@Injectable({
  providedIn: 'root'
})
export class ConfirmPasswordResetServiceService {
  private url = `${environment.apiUrl}/api/password_reset/confirm/`;

  constructor(private http: HttpClient) { }

  confirmPasswordReset(password: string, token: string): Observable<ResetConfirmationResponse> {
    const form_data = new FormData()
    form_data.append("password", password!)
    form_data.append("token", token)

    return this.http.post<ResetConfirmationResponse>(this.url, form_data)
  }
}
