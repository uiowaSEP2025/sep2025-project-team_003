import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { NgxExtendedPdfViewerModule, NgxExtendedPdfViewerService } from 'ngx-extended-pdf-viewer';
import { ActivatedRoute } from '@angular/router';
import { Observable, of, Subscription } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { LoadingFallbackComponent } from '../../components/loading-fallback/loading-fallback.component';
import { pdfDefaultOptions } from 'ngx-extended-pdf-viewer';

pdfDefaultOptions.assetsFolder = 'static';
@Component({
  selector: 'app-quote-sign',
  templateUrl: './quote-sign.component.html',
  styleUrls: ['./quote-sign.component.scss'],
  standalone: true,
  imports: [CommonModule, NgxExtendedPdfViewerModule, LoadingFallbackComponent]
})
export class QuoteSignComponent implements OnInit, OnDestroy {
  pdfBlobUrl$!: Observable<string | null>;
  public currentBlobUrl: string | null = null;
  private subs = new Subscription();
  private token!: string
  isSuccess = false

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private pdfService: NgxExtendedPdfViewerService
  ) {}

  ngOnInit() {
    // Access token from URL query params
    this.route.queryParamMap.subscribe(params => {
      const token = params.get('token');
      console.log('succ')
      if (token) {
        this.token = token
        // Fetch the PDF using the token
        this.pdfBlobUrl$ = this.http.post<{ quote_pdf_base64: string }>(
          'api/ret/quote', {"pin": token} // Adjust the endpoint based on the API
        ).pipe(
          map(resp => {
            // Convert base64 to binary data
            const binary = atob(resp.quote_pdf_base64);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) {
              bytes[i] = binary.charCodeAt(i); // Convert binary to byte array
            }
            const blob = new Blob([bytes], { type: 'application/pdf' }); // Create Blob
            return URL.createObjectURL(blob); // Generate object URL for PDF
          }),
          catchError((err: HttpErrorResponse) => {
            console.error('PDF fetch error', err);
            return of(null); // Return null if there's an error
          }),
          tap(url => this.currentBlobUrl = url) // Set the currentBlobUrl to display in template
        );

        this.subs.add(this.pdfBlobUrl$.subscribe()); // Subscribe to the PDF URL observable
      }
    });
  }

  ngOnDestroy() {
    // Unsubscribe to avoid memory leaks
    this.subs.unsubscribe();
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

    try {
      await this.http.post(`/api/quote/sign`, { signed_pdf_base64: base64, 
        token: this.token
       }).toPromise();
       this.isSuccess = true
      alert('Quote submitted successfully!');
      
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
