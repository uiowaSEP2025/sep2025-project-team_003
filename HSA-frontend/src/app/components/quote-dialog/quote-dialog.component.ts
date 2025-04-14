import { CommonModule } from '@angular/common';
import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ErrorHandlerService } from '../../services/error.handler.service';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-quote-dialog',
  // Ensure your standalone component includes all necessary modules
  imports: [
    CommonModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule
  ],
  templateUrl: './quote-dialog.component.html',
  styleUrls: ['./quote-dialog.component.scss']
})
export class QuoteDialogComponent {
  pdfUrl: SafeResourceUrl | null = null;
  isLoading = false;
  // Declare the recipients property so ngModel can bind to it.
  recipients: string = '';

  constructor(
    private http: HttpClient,
    private sanitizer: DomSanitizer,
    private errorHandler: ErrorHandlerService,
    public dialogRef: MatDialogRef<QuoteDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { jobID: number }
  ) {}

  generatePreview() {
    this.isLoading = true;
    this.http.get(`api/generate/quote/${this.data.jobID}`, { responseType: 'blob' })
      .subscribe({
        next: (blob) => {
          const url = URL.createObjectURL(blob);
          this.pdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
          this.isLoading = false;
        },
        error: (err) => {
          this.errorHandler.handleError(err);
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

  sendTo() {
    // Call the API using the recipient's information.
    this.http.get(`api/quotes/id/${this.recipients}`, { responseType: 'blob' })
      .subscribe({
        next: (blob) => {
          alert(`Quote sent successfully to ${this.recipients}`);
        },
        error: (err) => {
          this.errorHandler.handleError(err);
        }
      });
  }
}
