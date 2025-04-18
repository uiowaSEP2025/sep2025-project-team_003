import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { QuoteDialogComponent } from './quote-dialog.component';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { By } from '@angular/platform-browser';
import { DomSanitizer } from '@angular/platform-browser';

describe('QuoteDialogComponent', () => {
  let component: QuoteDialogComponent;
  let fixture: ComponentFixture<QuoteDialogComponent>;
  let httpMock: HttpTestingController;
  let dialogRefSpy: jasmine.SpyObj<MatDialogRef<QuoteDialogComponent>>;
  let sanitizer: DomSanitizer;

  beforeEach(async () => {
    dialogRefSpy = jasmine.createSpyObj('MatDialogRef', ['close']);

    await TestBed.configureTestingModule({
      imports: [
        QuoteDialogComponent,
        HttpClientTestingModule
      ],
      providers: [
        { provide: MatDialogRef,    useValue: dialogRefSpy },
        { provide: MAT_DIALOG_DATA, useValue: { jobID: 123 } }
      ]
    }).compileComponents();

    fixture    = TestBed.createComponent(QuoteDialogComponent);
    component  = fixture.componentInstance;
    httpMock   = TestBed.inject(HttpTestingController);
    sanitizer  = TestBed.inject(DomSanitizer);
    fixture.detectChanges();
  });

  afterEach(() => httpMock.verify());

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should generate preview and set pdfUrl', fakeAsync(() => {
    const btn = fixture.debugElement.query(By.css('button[color="primary"]')).nativeElement;
    btn.click();
    fixture.detectChanges();

    const req = httpMock.expectOne('api/generate/quote/123');
    expect(req.request.method).toBe('GET');
    req.flush(new Blob(['dummy'], { type: 'application/pdf' }));
    tick();
    fixture.detectChanges();

    expect(component.isLoading).toBeFalse();
    expect(component.pdfUrl).toBeTruthy();
    expect(fixture.debugElement.query(By.css('iframe'))).toBeTruthy();
  }));

  it('should download PDF when download button clicked', () => {
    // arrange: set a dummy pdfUrl via injected sanitizer, not component.sanitizer
    const dummyUrl = 'blob:http://localhost/dummy';
    component.pdfUrl = sanitizer.bypassSecurityTrustResourceUrl(dummyUrl);
    fixture.detectChanges();

    const downloadBtn = fixture.debugElement.query(By.css('button[color="accent"]')).nativeElement;

    spyOn(document, 'createElement').and.callFake((tag: string) => {
      expect(tag).toBe('a');
      // return a fake <a> that captures href/download and has a spyable click()
      return {
        set href(value: string) { expect(value).toBe(dummyUrl); },
        set download(filename: string) {
          expect(filename).toBe('quote-123.pdf');
        },
        click: jasmine.createSpy('click')
      } as any;
    });

    downloadBtn.click();
  });

  it('should send quote and handle success', fakeAsync(() => {
    const sendBtn = fixture.debugElement.query(By.css('button[color="warn"]')).nativeElement;
    sendBtn.click();
    fixture.detectChanges();
    expect(component.sendState).toBe('pending');

    const req = httpMock.expectOne('api/send/quote/123');
    expect(req.request.method).toBe('POST');
    req.flush({ success: true });
    tick();
    fixture.detectChanges();

    expect(component.sendState).toBe('success');
  }));

  it('should set error state on send failure', fakeAsync(() => {
    const sendBtn = fixture.debugElement.query(By.css('button[color="warn"]')).nativeElement;
    sendBtn.click();
    fixture.detectChanges();

    const req = httpMock.expectOne('api/send/quote/123');
    req.error(new ErrorEvent('Network error'));
    tick();
    fixture.detectChanges();

    expect(component.sendState).toBe('error');
  }));
});
