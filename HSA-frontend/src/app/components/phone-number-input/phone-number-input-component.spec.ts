import { ComponentFixture, TestBed } from '@angular/core/testing';
import { InternalInputManager } from './phone-number-input-component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

describe('TableComponentComponent', () => {
  let component: InternalInputManager;
  let fixture: ComponentFixture<InternalInputManager>;


  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InternalInputManager],
      providers: [provideAnimationsAsync()]
    })
      .compileComponents();

    fixture = TestBed.createComponent(InternalInputManager);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should be required when its empty', () => {
    const compiled = fixture.debugElement.nativeElement;
    const inputs = compiled.querySelectorAll('input')
    const area = inputs[0]
    area.dispatchEvent(new Event('blur'));
    fixture.detectChanges()
    const errorTextElement = compiled.querySelector('mat-error')
    expect(errorTextElement.textContent).toEqual('phone number is required')
  })

  it('should be invalid when there are are letters', () => {
    const compiled = fixture.debugElement.nativeElement;
    const inputs = compiled.querySelectorAll('input')
    const area = inputs[0]
    area.value = 'abc'
    area.dispatchEvent(new Event('input'));
    area.dispatchEvent(new Event('blur'));
    fixture.detectChanges()
    const errorTextElement = compiled.querySelector('mat-error')
    expect(errorTextElement.textContent).toEqual('phone number is invalid')
  })

  it('should be invalid when there it is too short', () => {
    const compiled = fixture.debugElement.nativeElement;
    const inputs = compiled.querySelectorAll('input')
    const area = inputs[0]
    area.value = '123'
    area.dispatchEvent(new Event('input'));
    area.dispatchEvent(new Event('blur'));
    fixture.detectChanges()
    const errorTextElement = compiled.querySelector('mat-error')
    expect(errorTextElement.textContent).toEqual('phone number is invalid')
  })

  it('should be valid with a valid phone number', () => {
    const compiled = fixture.debugElement.nativeElement;
    const inputs = compiled.querySelectorAll('input')
    const area = inputs[0]
    const exchange = inputs[1]
    const subscriber = inputs[2]
    area.value = '123'
    area.dispatchEvent(new Event('input'));
    area.dispatchEvent(new Event('blur'));
    exchange.value = '123'
    exchange.dispatchEvent(new Event('input'));
    exchange.dispatchEvent(new Event('blur'));
    subscriber.value = '1234'
    subscriber.dispatchEvent(new Event('input'));
    subscriber.dispatchEvent(new Event('blur'));
    fixture.detectChanges()
    const errorTextElement = compiled.querySelector('mat-error')
    expect(errorTextElement).toBe(null)

  })


});
