/**
 * DO NOT TOUCH THIS FILE! IT IS HELD TOGETHER BY DUCT-TAPE AND PRAYERS!
 * YOU BREAK IT YOU BUY IT!
 */
import { FocusMonitor } from '@angular/cdk/a11y';
import { coerceBooleanProperty } from '@angular/cdk/coercion';
import {
  Component,
  ElementRef,
  Input,
  OnDestroy,
  Optional,
  Self,
  ViewChild
} from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ControlValueAccessor,
  NgControl,
  Validators,
  FormControl,
  AbstractControl,
  ReactiveFormsModule
} from '@angular/forms';
import { MatFormFieldControl, MatLabel, MatFormFieldModule } from '@angular/material/form-field';
import { Subject } from 'rxjs';
import { MatIconModule } from '@angular/material/icon';
import { ValidatorFn } from '@angular/forms';

/** Custom `MatFormFieldControl` for telephone number input. */
@Component({
  selector: 'internal-input-manager',
  templateUrl: 'internal-input-manager.html',
  styleUrls: ['internal-input-manager.css'],
  providers: [{ provide: MatFormFieldControl, useExisting: InternalInputManager }],
  imports: [ReactiveFormsModule],
  host: {
    '[class.example-floating]': 'shouldLabelFloat',
    '[id]': 'id',
    '[attr.aria-describedby]': 'describedBy'
  }
})
export class InternalInputManager
  implements ControlValueAccessor, MatFormFieldControl<MyTel>, OnDestroy {
  static nextId = 0;
  @ViewChild('area') areaInput!: HTMLInputElement;
  @ViewChild('exchange') exchangeInput!: HTMLInputElement;
  @ViewChild('subscriber') subscriberInput!: HTMLInputElement;

  parts: FormGroup;
  stateChanges = new Subject<void>();
  focused = false;
  errorState = false;
  controlType = 'example-tel-input';
  id = `example-tel-input-${InternalInputManager.nextId++}`;
  describedBy = '';
  onChange = (_: any) => { };
  onTouched = () => { };

  isValid = () => {
    const {
      value: { area, exchange, subscriber }
    } = this.parts
    if (area === '' && subscriber === '' && exchange === '') {
      return false
    }
    if (area.length !== 3 || subscriber.length != 4 || exchange.length !== 3) {
      return false
    }
    if (isNaN(Number(area)) || isNaN(Number(subscriber)) || isNaN(Number(exchange))) {
      return false
    }
    return true
  }

  isEmpty = () => {
    const {
      value: { area, exchange, subscriber }
    } = this.parts
    return area === '' && subscriber === '' && exchange === '' ? true : false
  }

  get empty() {
    const {
      value: { area, exchange, subscriber }
    } = this.parts;

    return !area && !exchange && !subscriber;
  }

  get shouldLabelFloat() {
    return this.focused || !this.empty;
  }

  @Input()
  get placeholder(): string {
    return this._placeholder;
  }
  set placeholder(value: string) {
    this._placeholder = value;
    this.stateChanges.next();
  }
  private _placeholder!: string;

  @Input()
  get required(): boolean {
    return this._required;
  }
  set required(value: boolean) {
    this._required = coerceBooleanProperty(value);
    this.stateChanges.next();
  }
  private _required = false;

  @Input()
  get disabled(): boolean {
    return this._disabled;
  }
  set disabled(value: boolean) {
    this._disabled = coerceBooleanProperty(value);
    this._disabled ? this.parts.disable() : this.parts.enable();
    this.stateChanges.next();
  }
  private _disabled = false;

  @Input()
  get value(): MyTel | null {
    const {
      value: { area, exchange, subscriber }
    } = this.parts;
    return new MyTel(area, exchange, subscriber);
  }
  set value(tel: MyTel | null) {
    const { area, exchange, subscriber } = tel || new MyTel('', '', '');
    this.parts.setValue({ area, exchange, subscriber });
    this.stateChanges.next();
  }

  constructor(
    formBuilder: FormBuilder,
    private _focusMonitor: FocusMonitor,
    private _elementRef: ElementRef<HTMLElement>,
    @Optional() @Self() public ngControl: NgControl
  ) {
    this.parts = formBuilder.group({
      area: [
        null,
        [Validators.required, Validators.minLength(3), Validators.maxLength(3)]
      ],
      exchange: [
        null,
        [Validators.required, Validators.minLength(3), Validators.maxLength(3)]
      ],
      subscriber: [
        null,
        [Validators.required, Validators.minLength(4), Validators.maxLength(4)]
      ]
    });

    _focusMonitor.monitor(_elementRef, true).subscribe(origin => {
      if (this.focused && !origin) {
        this.onTouched();
      }
      this.focused = !!origin;
      this.stateChanges.next();
      if (origin === null) {
        // this is triggered when use clicks off the input
        this.errorState = !this.isValid()
      }
    });

    if (this.ngControl != null) {
      this.ngControl.valueAccessor = this;
    }
  }


  autoFocusNext(control: AbstractControl, nextElement?: HTMLInputElement): void {
    if (!control.errors && !!nextElement) {
      this._focusMonitor.focusVia(nextElement, 'program');
    }
  }

  autoFocusPrev(control: AbstractControl, prevElement: HTMLInputElement): void {
    if (control.value.length < 1) {
      this._focusMonitor.focusVia(prevElement, 'program');
    }
  }

  ngOnDestroy() {
    this.stateChanges.complete();
    this._focusMonitor.stopMonitoring(this._elementRef);
  }

  setDescribedByIds(ids: string[]) {
    this.describedBy = ids.join(' ');
  }

  onContainerClick(event: MouseEvent) {
    if (this.parts.controls['subscriber'].valid) {
      this._focusMonitor.focusVia(this.subscriberInput, 'program');
    } else if (this.parts.controls['exchange'].valid) {
      this._focusMonitor.focusVia(this.subscriberInput, 'program');
    } else if (this.parts.controls['area'].valid) {
      this._focusMonitor.focusVia(this.exchangeInput, 'program');
    } else {
      this._focusMonitor.focusVia(this.areaInput, 'program');
    }
  }

  writeValue(tel: MyTel | null): void {
    this.value = tel;
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  setDisabledState(isDisabled: boolean): void {
    this.disabled = isDisabled;
  }

  _handleInput(control: AbstractControl, nextElement?: HTMLInputElement): void {
    this.errorState = this.isEmpty()
    this.autoFocusNext(control, nextElement);
    this.onChange(this.value);
  }

  static ngAcceptInputType_disabled: boolean | string | null | undefined;
  static ngAcceptInputType_required: boolean | string | null | undefined;
}

const validateParentComponent: ValidatorFn = (control: AbstractControl) => {
  const val = control.value
  if (val.area === '' && val.subscriber === '' && val.exchange === '') {
    return { required: true }
  }
  if (val.area.length !== 3 || val.subscriber.length !== 4 || val.exchange.length !== 3) {
    return { invalid: true }
  }
  if (isNaN(Number(val.area)) || isNaN(Number(val.subscriber)) || isNaN(Number(val.exchange))) {
    return { invalid: true }
  }
  return null
}



/** Data structure for holding telephone number. */
export class MyTel {
  constructor(
    public area: string,
    public exchange: string,
    public subscriber: string
  ) { }
}