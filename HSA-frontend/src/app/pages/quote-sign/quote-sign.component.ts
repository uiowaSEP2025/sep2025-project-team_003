import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { NgxExtendedPdfViewerModule } from 'ngx-extended-pdf-viewer';
import { ReactiveFormsModule } from '@angular/forms';
import { Observable, Subject } from 'rxjs';
import { switchMap, map, tap, catchError } from 'rxjs/operators';

@Component({
  selector: 'app-quote-sign',
  templateUrl: './quote-sign.component.html',
  styleUrls: ['./quote-sign.component.scss'],
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgxExtendedPdfViewerModule,
  ]
})
export class QuoteSignComponent implements OnInit {
  form!: FormGroup;

  private submit$ = new Subject<{ quoteId: string; pin: string }>();

  pdfBlobUrl$: Observable<string | null>;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient
  ) {
    this.pdfBlobUrl$ = this.submit$.pipe(
      switchMap(({ quoteId, pin }) => {
        const url = `api/ret/quote/${quoteId}`;
        return this.http.post(url, { pin }, { responseType: 'blob' }).pipe(
          map(blob => {
            // create a fresh blob URL
            return URL.createObjectURL(new Blob([blob], { type: 'application/pdf' }));
          }),

          catchError((err: HttpErrorResponse) => {
            console.error('Error fetching PDF', err);
            return [null];
          })
        );
      })
    );
  }

  ngOnInit() {
    this.form = this.fb.group({
      quoteId: ['', Validators.required],
      pin: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.form.invalid) {
      return;
    }
    this.submit$.next(this.form.value);
  }
}
