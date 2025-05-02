// quote-sign.component.ts
import {
  Component,
  OnInit,
  OnDestroy,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule
} from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import {
  NgxExtendedPdfViewerModule
} from 'ngx-extended-pdf-viewer';

import { Observable, Subject, of, Subscription } from 'rxjs';
import { switchMap, map, catchError, tap } from 'rxjs/operators';
import { pdfDefaultOptions } from 'ngx-extended-pdf-viewer';

pdfDefaultOptions.assetsFolder = 'static';

@Component({
  selector: 'app-quote-sign',
  templateUrl: './quote-sign.component.html',
  styleUrls: ['./quote-sign.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    NgxExtendedPdfViewerModule
  ]
})
export class QuoteSignComponent implements OnInit, OnDestroy {
  form!: FormGroup;

  /** The blob URL emitted by the pipeline (or null on error) */
  pdfBlobUrl$: Observable<string | null>;

  /** Holds the latest non-null blob URL so we can fetch it */
  public currentBlobUrl: string | null = null;

  /** For driving the HTTP-fetch pipeline */
  private submit$ = new Subject<{ quoteId: string; pin: string }>();

  /** Manage our subscriptions */
  private subs = new Subscription();

  constructor(
    private fb: FormBuilder,
    private http: HttpClient
  ) {
    // Build the fetch-&-decode pipeline
    this.pdfBlobUrl$ = this.submit$.pipe(
      switchMap(({ quoteId, pin }) =>
        this.http
          .post<{ quote_pdf_base64: string }>(
            `/api/ret/quote/${quoteId}`,
            { pin }
          )
          .pipe(
            map(resp => {
              // Base64 → binary → Blob → blob URL
              const binary = atob(resp.quote_pdf_base64);
              const bytes  = new Uint8Array(binary.length);
              for (let i = 0; i < binary.length; i++) {
                bytes[i] = binary.charCodeAt(i);
              }
              const blob = new Blob([bytes], { type: 'application/pdf' });
              return URL.createObjectURL(blob);
            }),
            catchError((err: HttpErrorResponse) => {
              console.error('PDF fetch error', err);
              return of(null);
            })
          )
      ),
      // Remember the latest URL so we can re-fetch it later
      tap(url => this.currentBlobUrl = url)
    );

    // Subscribe so the pipeline actually runs when we .next()
    this.subs.add(this.pdfBlobUrl$.subscribe());
  }

  ngOnInit() {
    this.form = this.fb.group({
      quoteId: ['', Validators.required],
      pin:     ['', Validators.required]
    });
  }

  ngOnDestroy() {
    this.subs.unsubscribe();
  }

  /** Called by the form’s (ngSubmit) to fetch the PDF */
  onSubmit() {
    if (this.form.valid) {
      this.submit$.next(this.form.value);
    }
  }

  /** Called by the “Submit Quote” button after the PDF is loaded */
  async submitQuote() {
    if (!this.currentBlobUrl) {
      console.error('No PDF to submit');
      return;
    }
  
    try {
      const arrayBuffer = await fetch(this.currentBlobUrl).then(r => r.arrayBuffer());
      const binary = new Uint8Array(arrayBuffer)
        .reduce((s, byte) => s + String.fromCharCode(byte), '');
      const base64 = btoa(binary);
  
      const quoteId = this.form.get('quoteId')!.value;
      await this.http.post(`/api/quote/sign/${quoteId}`, {
        signed_pdf_base64: base64
      }).toPromise();
  
      // show confirmation (optional)
      alert('Quote submitted successfully!');
  
      // reload the page
      window.location.reload();
    } catch (err) {
      console.error('Error submitting quote', err);
      alert('Failed to submit quote.');
    }
  }
  



  onConfirmSubmit() {
    // first confirmation
    if (!confirm('Are you sure you want to submit this quote?')) {
      return;
    }
  
    // finally, call your existing submit function
    this.submitQuote();
  }
}
