import { CommonModule } from '@angular/common';
import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

type SendState = 'pending' | 'success' | 'error' | '';

@Component({
  selector: 'app-quote-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatButtonModule,
  ],
  templateUrl: './quote-dialog.component.html',
  styleUrls: ['./quote-dialog.component.scss']
})
export class QuoteDialogComponent {
  pdfUrl: SafeResourceUrl | null = null;
  isLoading = false;
  sendState: SendState = '';

  recipients: string = '';

  constructor(
    private http: HttpClient,
    private sanitizer: DomSanitizer,
    public dialogRef: MatDialogRef<QuoteDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { jobID: number }
  ) {}

  generatePreview() {
    this.isLoading = true;
    this.http.get(`api/generate/quote/${this.data.jobID}`, { responseType: 'blob' })
      .subscribe({
        next: blob => {
          const url = URL.createObjectURL(blob);
          this.pdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
          this.isLoading = false;
        },
        error: () => {
          this.isLoading = false;
        }
      });
  }

  downloadPdf() {
    if (this.pdfUrl) {
      const link = document.createElement('a');
      link.href = (this.pdfUrl as any).changingThisBreaksApplicationSecurity;
      link.download = `quote-${this.data.jobID}.pdf`;
      link.click();
    }
  }

  send() {
    this.sendState = 'pending';

    this.http
      .post<{ success: boolean; message?: string }>(
        `api/send/quote/${this.data.jobID}`,
        {},
        { responseType: 'json' }
      )
      .subscribe({
        next: res => {
          this.sendState = res.success ? 'success' : 'error';
        },
        error: err => {
          console.error('Send failed', err);
          this.sendState = 'error';
        }
      });
  }
}
