import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { NgxExtendedPdfViewerModule, NgxExtendedPdfViewerService } from 'ngx-extended-pdf-viewer';
import { Observable, Subject, Subscription, of } from 'rxjs';
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
  pdfBlobUrl$: Observable<string | null>;
  public currentBlobUrl: string | null = null;
  private submit$ = new Subject<{ quoteId: string; pin: string }>();
  private subs = new Subscription();

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private pdfService: NgxExtendedPdfViewerService
  ) {
    this.pdfBlobUrl$ = this.submit$.pipe(
      switchMap(({ quoteId, pin }) =>
        this.http.post<{ quote_pdf_base64: string }>(
          `/api/ret/quote/${quoteId}`, { pin }
        ).pipe(
          map(resp => {
            const binary = atob(resp.quote_pdf_base64);
            const bytes = new Uint8Array(binary.length);
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
      tap(url => this.currentBlobUrl = url)
    );

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

  onSubmit() {
    if (this.form.valid) {
      this.submit$.next(this.form.value);
    }
  }

  async submitQuote() {
    let blob: Blob | undefined;
    blob = await this.pdfService.getCurrentDocumentAsBlob();

    let arrayBuffer: ArrayBuffer;
    if (blob && blob.arrayBuffer) {
      arrayBuffer = await blob.arrayBuffer();
    } else {
      const encoder = new TextEncoder();
      arrayBuffer = encoder.encode('hello world').buffer;
    }

    const bytes = new Uint8Array(arrayBuffer);
    let binary = '';
    for (const b of bytes) {
      binary += String.fromCharCode(b);
    }
    const base64 = btoa(binary);

    const quoteId = this.form.get('quoteId')!.value;
    try {
      await this.http.post(`/api/quote/sign/${quoteId}`, { signed_pdf_base64: base64 }).toPromise();
      alert('Quote submitted successfully!');
      this.creload()
    } catch (err) {
      console.error('Error submitting quote', err);
      alert('Failed to submit quote.');
    }
  }

  creload() {
    window.location.reload()
  }

  onConfirmSubmit() {
    if (!confirm('Are you sure you want to submit this quote?')) {
      return;
    }
    this.submitQuote();
  }
}
