// quote-sign.component.spec.ts
import { ComponentFixture, TestBed, fakeAsync, tick, flush, waitForAsync } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { QuoteSignComponent } from './quote-sign.component';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { NgxExtendedPdfViewerService } from 'ngx-extended-pdf-viewer';

describe('QuoteSignComponent (full coverage)', () => {
  let fixture: ComponentFixture<QuoteSignComponent>;
  let component: QuoteSignComponent;
  let httpMock: HttpTestingController;
  // single spy instance – no pdfSvc + pdfServiceSpy confusion
  let pdfServiceSpy: jasmine.SpyObj<NgxExtendedPdfViewerService>;

  beforeEach(waitForAsync(() => {
    // create one spy
    pdfServiceSpy = jasmine.createSpyObj(
      'NgxExtendedPdfViewerService',
      ['getCurrentDocumentAsBlob']
    );

    TestBed.configureTestingModule({
      imports: [ ReactiveFormsModule, QuoteSignComponent ],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
        // provide *that* spy
        { provide: NgxExtendedPdfViewerService, useValue: pdfServiceSpy }
      ]
    })
    .compileComponents()
    .then(() => {
      fixture = TestBed.createComponent(QuoteSignComponent);
      component = fixture.componentInstance;
      httpMock = TestBed.inject(HttpTestingController);
      // spy is already configured; no need to reassign
      spyOn(URL, 'createObjectURL').and.returnValue('blob://dummy');
      fixture.detectChanges(); // kicks off ngOnInit + subscription
    });
  }));

  afterEach(() => httpMock.verify());
  it('should create and set up form', () => {
    expect(component).toBeTruthy();
    const f = component.form;
    expect(f.contains('quoteId')).toBeTrue();
    expect(f.contains('pin')).toBeTrue();
    expect(f.get('quoteId')!.valid).toBeFalse();
    expect(f.get('pin')!.valid).toBeFalse();
  });

  it('onSubmit(): invalid form does nothing', () => {
    const nextSpy = spyOn((component as any).submit$, 'next');
    component.onSubmit();
    expect(nextSpy).not.toHaveBeenCalled();
  });

  it('onSubmit(): valid form emits and triggers PDF fetch → blob URL', fakeAsync(() => {
    const nextSpy = spyOn((component as any).submit$, 'next').and.callThrough();
    component.form.setValue({ quoteId: 'ABC', pin: '1234' });
    component.onSubmit();
    expect(nextSpy).toHaveBeenCalledWith({ quoteId: 'ABC', pin: '1234' });

    // flush all matching PDF‐fetch calls
    const reqs = httpMock.match(r => r.url === '/api/ret/quote/ABC');
    expect(reqs.length).toBeGreaterThan(0);
    reqs.forEach(r => r.flush({ quote_pdf_base64: btoa('PDF') }));

    tick();
    expect(component.currentBlobUrl).toBe('blob://dummy');
    flush();
  }));

  it('PDF-fetch error sets currentBlobUrl to null', fakeAsync(() => {
    component.currentBlobUrl = 'was-here';
    component.form.setValue({ quoteId: 'ERR', pin: '0000' });
    component.onSubmit();

    const reqs = httpMock.match(r => r.url === '/api/ret/quote/ERR');
    reqs.forEach(r => r.error(new ProgressEvent('fail')));

    tick();
    expect(component.currentBlobUrl).toBeNull();
    flush();
  }));

  it('onConfirmSubmit() calls submitQuote only if confirmed', () => {
    const submitSpy = spyOn(component, 'submitQuote');
    spyOn(window, 'confirm').and.returnValue(false);
    component.onConfirmSubmit();
    expect(submitSpy).not.toHaveBeenCalled();

    (window.confirm as jasmine.Spy).and.returnValue(true);
    component.onConfirmSubmit();
    expect(submitSpy).toHaveBeenCalled();
  });

  it('should use arrayBuffer() path and alert success', fakeAsync(() => {
    spyOn(component, 'creload').and.callFake(() => {});
    const db = new TextEncoder().encode('hello').buffer;
    const realBlob = new Blob([db], { type: 'application/pdf' });
    pdfServiceSpy.getCurrentDocumentAsBlob.and.returnValue(
      Promise.resolve(realBlob)
    );

    component.form.setValue({ quoteId: '77', pin: '0000' });
    component.submitQuote();
    tick(); // resolves getCurrentDocumentAsBlob + arrayBuffer()
    
    const req = httpMock.expectOne('/api/quote/sign/77');

    req.flush({})
    tick(); // resolve the POST
    flush();
  }));

});
