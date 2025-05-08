import { ComponentFixture, TestBed, fakeAsync, tick, flush, waitForAsync } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { QuoteSignComponent } from './quote-sign.component';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { NgxExtendedPdfViewerService } from 'ngx-extended-pdf-viewer';
import { of, Subject } from 'rxjs';
import { ActivatedRoute, convertToParamMap } from '@angular/router';

describe('QuoteSignComponent (full coverage)', () => {
  let fixture: ComponentFixture<QuoteSignComponent>;
  let component: QuoteSignComponent;
  let httpMock: HttpTestingController;
  let pdfServiceSpy: jasmine.SpyObj<NgxExtendedPdfViewerService>;
  let paramMapSubject: Subject<any>;

  beforeEach(waitForAsync(() => {
    paramMapSubject = new Subject();
    const activatedRouteMock = {
      queryParamMap: paramMapSubject.asObservable(),
      queryParams: of({})
    };

    pdfServiceSpy = jasmine.createSpyObj('NgxExtendedPdfViewerService', ['getCurrentDocumentAsBlob']);

    TestBed.configureTestingModule({
      imports: [ReactiveFormsModule, QuoteSignComponent],
      providers: [
        provideAnimationsAsync(),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: NgxExtendedPdfViewerService, useValue: pdfServiceSpy },
        { provide: ActivatedRoute, useValue: activatedRouteMock }
      ]
    }).compileComponents().then(() => {
      fixture = TestBed.createComponent(QuoteSignComponent);
      component = fixture.componentInstance;
      httpMock = TestBed.inject(HttpTestingController);
      spyOn(URL, 'createObjectURL').and.returnValue('blob://dummy');
      fixture.detectChanges();
      paramMapSubject.next(convertToParamMap({ token: 'myTokenValue' }));
    });
  }));

  afterEach(() => {});

  it('PDF-fetch error sets currentBlobUrl to null', fakeAsync(() => {
    tick();
    const req = httpMock.expectOne('api/ret/quote');
    req.error(new ProgressEvent('error'));
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
    spyOn(window, 'alert');
    const db = new TextEncoder().encode('hello').buffer;
    const realBlob = new Blob([db], { type: 'application/pdf' });
    pdfServiceSpy.getCurrentDocumentAsBlob.and.returnValue(Promise.resolve(realBlob));
    component['token'] = '77';

    component.submitQuote();
    tick();

    const req = httpMock.expectOne('/api/quote/sign');
    expect(req.request.body.token).toBe('77');
    req.flush({});
    tick();
    expect(window.alert).toHaveBeenCalledWith('Quote submitted successfully!');
    flush();
  }));
});
