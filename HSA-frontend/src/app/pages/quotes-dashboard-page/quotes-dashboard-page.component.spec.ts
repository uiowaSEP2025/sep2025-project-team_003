// quotes-dashboard-page.component.spec.ts

import { TestBed, ComponentFixture, fakeAsync, tick } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { QuotesDashboardPageComponent } from './quotes-dashboard-page.component';

describe('QuotesDashboardPageComponent (standalone)', () => {
  let fixture: ComponentFixture<QuotesDashboardPageComponent>;
  let component: QuotesDashboardPageComponent;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        QuotesDashboardPageComponent,    // <-- import standalone component here
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(QuotesDashboardPageComponent);
    component = fixture.componentInstance;
    httpMock  = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should load quotes on init (no filter)', fakeAsync(() => {
    const mockData = [{
      job_id: 1,
      customer_name: 'Alice',
      quote_status: 'new',
      quote_s3_link: null,
      start_date: null,
      end_date: null
    }];

    fixture.detectChanges(); // ngOnInit → loadQuotes()
    const req = httpMock.expectOne('/api/get/quotes');
    expect(req.request.method).toBe('GET');
    req.flush({ data: mockData });
    tick();
    expect(component.quotes).toEqual(mockData);
  }));

  it('should include filter in URL when filter is set', fakeAsync(() => {
    component.filter = 'open';
    component.loadQuotes();
    const req = httpMock.expectOne('/api/get/quotes?filterby=open');
    expect(req.request.method).toBe('GET');
    req.flush({ data: [] });
    tick();
    expect(component.quotes).toEqual([]);
  }));

  it('applyFilter should update filter and reload', () => {
    spyOn(component, 'loadQuotes');
    component.applyFilter('accepted');
    expect(component.filter).toBe('accepted');
    expect(component.loadQuotes).toHaveBeenCalled();
  });

  describe('openQuote()', () => {
    let originalWindowOpen: any;
    let fakeWindow: any;

    beforeEach(() => {
      fakeWindow = { document: { write: jasmine.createSpy('write') } };
      originalWindowOpen = window.open;
      spyOn(window, 'open').and.returnValue(fakeWindow);
    });
    afterEach(() => {
      window.open = originalWindowOpen;
    });

    it('opens a new window and writes iframe HTML on success', fakeAsync(() => {
      const quote = {
        job_id: 42,
        customer_name: 'Bob',
        quote_status: 'new',
        quote_s3_link: null,
        start_date: null,
        end_date: null
      };

      component.openQuote(quote);
      const req = httpMock.expectOne('/api/render/quote/42');
      expect(req.request.method).toBe('GET');
      req.flush({ url: 'https://cdn.example.com/quotes/42.pdf' });
      tick();

      expect(window.open).toHaveBeenCalledWith('', '_blank');
      const html = fakeWindow.document.write.calls.mostRecent().args[0] as string;
      expect(html).toContain(`iframe src="https://cdn.example.com/quotes/42.pdf"`);
      expect(html).toContain(`function accept()`);
      expect(html).toContain(`function reject()`);
    }));

    it('alerts on error fetching PDF', fakeAsync(() => {
      spyOn(window, 'alert');
      const quote = {
        job_id: 7,
        customer_name: 'Carol',
        quote_status: 'new',
        quote_s3_link: null,
        start_date: null,
        end_date: null
      };

      component.openQuote(quote);
      const req = httpMock.expectOne('/api/render/quote/7');
      req.flush('Not found', { status: 404, statusText: 'Not Found' });
      tick();

      expect(window.alert).toHaveBeenCalledWith('Failed to fetch quote PDF.');
    }));
  });
});
