import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
interface Quote {
  job_id: number;
  customer_name: string;
  quote_status: string;
  quote_s3_link: string | null;
  start_date: string | null;
  end_date: string | null;
}

@Component({
  selector: 'app-quotes-dashboard',
  templateUrl: './quotes-dashboard-page.component.html',
  styleUrls: ['./quotes-dashboard-page.component.scss'],
  imports: [CommonModule]
})
export class QuotesDashboardPageComponent implements OnInit {
  quotes: Quote[] = [];
  filter: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadQuotes();
  }

  loadQuotes() {
    const url = this.filter ? `/api/get/quotes?filterby=${this.filter}` : `/api/get/quotes`;
    this.http.get<{ data: Quote[] }>(url).subscribe({
      next: res => {
        this.quotes = res.data;
      },
      error: err => console.error('Failed to load quotes:', err)
    });
  }
  
  

  applyFilter(filter: string) {
    this.filter = filter;
    this.loadQuotes();
  }

  openQuote(quote: Quote) {
    this.http.get<{ url: string }>(`/api/render/quote/${quote.job_id}`).subscribe({
      next: ({ url }) => {
        const win = window.open('', '_blank');
        if (win) {
          win.document.write(`
            <html>
              <body style="margin:0;padding:0">
                <iframe src="${url}" style="width:100vw;height:90vh;border:none;"></iframe>
                <div style="text-align:center;margin-top:10px">
                  <button onclick="accept()">Accept</button>
                  <button onclick="reject()">Reject</button>
                </div>
                <script>
                  function accept() {
                    fetch('/api/manage/quote/${quote.job_id}', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ decision: 'accept' })
                    }).then(res => location.reload());
                  }
                  function reject() {
                    fetch('/api/manage/quote/${quote.job_id}', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ decision: 'reject' })
                    }).then(res => location.reload());
                  }
                </script>
              </body>
            </html>
          `);
        }
      },
      error: err => alert('Failed to fetch quote PDF.')
    });
  }
}
