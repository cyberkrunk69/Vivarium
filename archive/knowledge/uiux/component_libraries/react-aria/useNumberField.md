# useNumberField

Source: https://react-spectrum.adobe.com/react-aria/useNumberField.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../NumberField).

# useNumberField

Provides the behavior and accessibility implementation for a number field component.
Number fields allow users to enter a number, and increment or decrement the value using stepper buttons.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useNumberField} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/spinbutton/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/numberfield "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/numberfield "View package")

## API[#](#api)

---

`useNumberField(
props: AriaNumberFieldProps,
state: NumberFieldState,
inputRef: RefObject<HTMLInputElement
|Â  |Â null>
): NumberFieldAria`

## Features[#](#features)

---

Number fields can be built with `<input type="number">`, but the behavior is very inconsistent across
browsers and platforms, it supports limited localized formatting options, and it is challenging to style
the stepper buttons. `useNumberField` helps achieve accessible number fields that support internationalized
formatting options and can be styled as needed.

- Support for internationalized number formatting and parsing including decimals, percentages, currency values, and units
- Support for the Latin, Arabic, and Han positional decimal numbering systems in [over 30 locales](../quality#supported-locales)
- Automatically detects the numbering system used and supports parsing numbers not in the default numbering system for the locale
- Support for multiple currency formats including symbol, code, and name in standard or accounting notation
- Validates keyboard entry as the user types so that only valid numeric input according to the locale and numbering system is accepted
- Handles composed input from input method editors, e.g. Pinyin
- Automatically selects an appropriate software keyboard for mobile according to the current platform and allowed values
- Supports rounding to a configurable number of fraction digits
- Support for clamping the value between a configurable minimum and maximum, and snapping to a step value
- Support for stepper buttons and arrow keys to increment and decrement the value according to the step value
- Supports pressing and holding the stepper buttons to continuously increment or decrement
- Handles floating point rounding errors when incrementing, decrementing, and snapping to step
- Supports using the scroll wheel to increment and decrement the value
- Exposed to assistive technology as a text field with a custom localized role description using ARIA
- Follows the [spinbutton](https://www.w3.org/WAI/ARIA/apg/patterns/spinbutton/) ARIA pattern
- Works around bugs in VoiceOver with the spinbutton role
- Uses an ARIA live region to ensure that value changes are announced
- Support for native HTML constraint validation with customizable UI, custom validation functions, realtime validation, and server-side validation errors

Read our [blog post](../blog/how-we-internationalized-our-numberfield) for more details about the interactions and internationalization support implemented by `useNumberField`.

## Anatomy[#](#anatomy)

---

Number fields consist of an input element that shows the current value and allows the user to type a new value,
optional stepper buttons to increment and decrement the value, a group containing the input and stepper buttons,
and a label.

`useNumberField` also supports optional description and error message elements, which can be used
to provide more context about the field, and any validation messages. These are linked with the
input via the `aria-describedby` attribute.

`useNumberField` returns props for each of these, which you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label element. |
| `groupProps` | `GroupDOMAttributes` | Props for the group wrapper around the input and stepper buttons. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `incrementButtonProps` | `AriaButtonProps` | Props for the increment button, to be passed to `useButton`. |
| `decrementButtonProps` | `AriaButtonProps` | Props for the decrement button, to be passed to `useButton`. |
| `descriptionProps` | `DOMAttributes` | Props for the number field's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the number field's error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

State is managed by the `useNumberFieldState`
hook from `@react-stately/numberfield`. The state object should be passed as an option to `useNumberField`

If there is no visual label, an `aria-label` or `aria-labelledby` prop must be passed instead
to identify the element to screen readers.

## Example[#](#example)

---

The following example shows how to build a simple number field. It includes an input element where the user can
type a number, along with increment and decrement buttons on either side. The `Button` component used in this example
is independent and can be used separately from `NumberField`.

**Note:** Due to [a bug](https://bugs.webkit.org/show_bug.cgi?id=219188) in Safari on macOS, pointer events may not
be dispatched after a `<button>` element is disabled while the mouse is pressed. This may require the user to click
twice when incrementing or decrementing the value from the minimum or maximum value. While out of scope for this example,
you may wish to use a `<div>` element instead of a `<button>` to avoid this issue. See the [useButton docs](../Button/useButton.html#custom-element-type)
for an example of a button with a custom element type.

In addition, see [useTextField](../TextField/useTextField.html) for an example of the description and error message elements.

```
import {useNumberFieldState} from 'react-stately';
import {useLocale, useNumberField} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function NumberField(props) {
  let { locale } = useLocale();
  let state = useNumberFieldState({ ...props, locale });
  let inputRef = React.useRef(null);
  let {
    labelProps,
    groupProps,
    inputProps,
    incrementButtonProps,
    decrementButtonProps
  } = useNumberField(props, state, inputRef);

  return (
    <div>
      <label {...labelProps}>{props.label}</label>
      <div {...groupProps}>
        <Button {...decrementButtonProps}>-</Button>
        <input {...inputProps} ref={inputRef} />
        <Button {...incrementButtonProps}>+</Button>
      </div>
    </div>
  );
}

<NumberField
  label="Price"
  defaultValue={6}
  formatOptions={{
    style: 'currency',
    currency: 'USD'
  }}
/>
```

```
import {useNumberFieldState} from 'react-stately';
import {useLocale, useNumberField} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function NumberField(props) {
  let { locale } = useLocale();
  let state = useNumberFieldState({ ...props, locale });
  let inputRef = React.useRef(null);
  let {
    labelProps,
    groupProps,
    inputProps,
    incrementButtonProps,
    decrementButtonProps
  } = useNumberField(props, state, inputRef);

  return (
    <div>
      <label {...labelProps}>{props.label}</label>
      <div {...groupProps}>
        <Button {...decrementButtonProps}>-</Button>
        <input {...inputProps} ref={inputRef} />
        <Button {...incrementButtonProps}>+</Button>
      </div>
    </div>
  );
}

<NumberField
  label="Price"
  defaultValue={6}
  formatOptions={{
    style: 'currency',
    currency: 'USD'
  }}
/>
```

```
import {useNumberFieldState} from 'react-stately';
import {
  useLocale,
  useNumberField
} from 'react-aria';

// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function NumberField(
  props
) {
  let { locale } =
    useLocale();
  let state =
    useNumberFieldState({
      ...props,
      locale
    });
  let inputRef = React
    .useRef(null);
  let {
    labelProps,
    groupProps,
    inputProps,
    incrementButtonProps,
    decrementButtonProps
  } = useNumberField(
    props,
    state,
    inputRef
  );

  return (
    <div>
      <label
        {...labelProps}
      >
        {props.label}
      </label>
      <div
        {...groupProps}
      >
        <Button
          {...decrementButtonProps}
        >
          -
        </Button>
        <input
          {...inputProps}
          ref={inputRef}
        />
        <Button
          {...incrementButtonProps}
        >
          +
        </Button>
      </div>
    </div>
  );
}

<NumberField
  label="Price"
  defaultValue={6}
  formatOptions={{
    style: 'currency',
    currency: 'USD'
  }}
/>
```

### Button[#](#button)

The `Button` component is used in the above example to increment and decrement the value. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

 Show code

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
  let { buttonProps } = useButton(props, ref);
  return <button {...buttonProps} ref={ref}>{props.children}</button>;
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(null);
  let { buttonProps } = useButton(props, ref);
  return (
    <button {...buttonProps} ref={ref}>
      {props.children}
    </button>
  );
}
```

```
import {useButton} from 'react-aria';

function Button(props) {
  let ref = React.useRef(
    null
  );
  let { buttonProps } =
    useButton(
      props,
      ref
    );
  return (
    <button
      {...buttonProps}
      ref={ref}
    >
      {props.children}
    </button>
  );
}
```

## Usage[#](#usage)

---

The following examples show how to use the `NumberField` component created in the above example.

### Controlled[#](#controlled)

By default, `NumberField` is uncontrolled. However, when using the `value` prop, it becomes controlled.
This allows you to store the current value in your own state, and use it elsewhere.

The `onChange` event is triggered whenever the number value updates. This happens when the user types a
value and blurs the input, or when incrementing or decrementing the value. It does not happen as the user
types because partial input may not be parseable to a valid number.

```
function Example() {
  let [value, setValue] = React.useState(6);

  return (
    <>
      <NumberField
        label="Controlled value"
        value={value}
        onChange={setValue} />
      <div>Current value prop: {value}</div>
    </>
  );
}
```

```
function Example() {
  let [value, setValue] = React.useState(6);

  return (
    <>
      <NumberField
        label="Controlled value"
        value={value}
        onChange={setValue} />
      <div>Current value prop: {value}</div>
    </>
  );
}
```

```
function Example() {
  let [value, setValue] =
    React.useState(6);

  return (
    <>
      <NumberField
        label="Controlled value"
        value={value}
        onChange={setValue}
      />
      <div>
        Current value
        prop: {value}
      </div>
    </>
  );
}
```

### Decimals[#](#decimals)

The default formatting style for `NumberField` is decimal, but you can configure various aspects via the `formatOptions`
prop. All options supported by [Intl.NumberFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat)
are supported, including configuration of minimum and maximum fraction digits, sign display, grouping separators, etc.
Currently only standard notation is supported, though scientific, engineering, and compact notation may be supported in the future.

The following example uses the `signDisplay` option to include the plus sign for positive numbers, for example to display
an offset from some value. In addition, it always displays a minimum of 1 digit after the decimal point, and allows up to
2 fraction digits. If the user enters more than 2 fraction digits, the result will be rounded.

```
<NumberField
  label="Adjust exposure"
  defaultValue={0}
  formatOptions={{
    signDisplay: 'exceptZero',
    minimumFractionDigits: 1,
    maximumFractionDigits: 2
  }} />
```

```
<NumberField
  label="Adjust exposure"
  defaultValue={0}
  formatOptions={{
    signDisplay: 'exceptZero',
    minimumFractionDigits: 1,
    maximumFractionDigits: 2
  }} />
```

```
<NumberField
  label="Adjust exposure"
  defaultValue={0}
  formatOptions={{
    signDisplay:
      'exceptZero',
    minimumFractionDigits:
      1,
    maximumFractionDigits:
      2
  }}
/>
```

### Percentages[#](#percentages)

The `style: 'percent'` option can be passed to the `formatOptions` prop to treat the value as a percentage. In this mode,
the value is multiplied by 100 before it is displayed, i.e. `0.45` is displayed as `45%`. The reverse is also true: when the
user enters a value, the `onChange` event will be triggered with the entered value divided by 100. When the percent option
is enabled, the default step automatically changes to `0.01` such that incrementing and decrementing occurs by `1%`. This can
be overridden with the `step` prop. [See below](#step-values) for details.

```
<NumberField
  label="Sales tax"
  defaultValue={0.05}
  formatOptions={{
    style: 'percent'
  }} />
```

```
<NumberField
  label="Sales tax"
  defaultValue={0.05}
  formatOptions={{
    style: 'percent'
  }} />
```

```
<NumberField
  label="Sales tax"
  defaultValue={0.05}
  formatOptions={{
    style: 'percent'
  }} />
```

### Currency values[#](#currency-values)

The `style: 'currency'` option can be passed to the `formatOptions` prop to treat the value as a currency value. The `currency`
option must also be passed to set the currency code (e.g. `USD`) to use. In addition, the `currencyDisplay` option can be
used to choose whether to display the currency symbol, currency code, or currency name. Finally, the `currencySign` option
can be set to `accounting` to use accounting notation for negative numbers, which uses parentheses rather than a minus sign
in some locales.

If you need to allow the user to change the currency, you should include a separate dropdown next to the number field.
The number field itself will not determine the currency from the user input.

```
<NumberField
  label="Transaction amount"
  defaultValue={45}
  formatOptions={{
    style: 'currency',
    currency: 'EUR',
    currencyDisplay: 'code',
    currencySign: 'accounting'
  }} />
```

```
<NumberField
  label="Transaction amount"
  defaultValue={45}
  formatOptions={{
    style: 'currency',
    currency: 'EUR',
    currencyDisplay: 'code',
    currencySign: 'accounting'
  }} />
```

```
<NumberField
  label="Transaction amount"
  defaultValue={45}
  formatOptions={{
    style: 'currency',
    currency: 'EUR',
    currencyDisplay:
      'code',
    currencySign:
      'accounting'
  }}
/>
```

### Units[#](#units)

The `style: 'unit'` option can be passed to the `formatOptions` prop to format the value with a unit of measurement. The `unit`
option must also be passed to set which unit to use (e.g. `inch`). In addition, the `unitDisplay` option can be used to choose
whether to display the unit in long, short, or narrow format.

If you need to allow the user to change the unit, you should include a separate dropdown next to the number field.
The number field itself will not determine the unit from the user input.

**Note:** the unit style is not currently supported in Safari. A [polyfill](https://formatjs.io/docs/polyfills/intl-numberformat/)
may be necessary.

```
<NumberField
  label="Package width"
  defaultValue={4}
  formatOptions={{
    style: 'unit',
    unit: 'inch',
    unitDisplay: 'long'
  }} />
```

```
<NumberField
  label="Package width"
  defaultValue={4}
  formatOptions={{
    style: 'unit',
    unit: 'inch',
    unitDisplay: 'long'
  }} />
```

```
<NumberField
  label="Package width"
  defaultValue={4}
  formatOptions={{
    style: 'unit',
    unit: 'inch',
    unitDisplay: 'long'
  }} />
```

### Minimum and maximum values[#](#minimum-and-maximum-values)

The `minValue` and `maxValue` props can be used to limit the entered value to a specific range. The value will be clamped
when the user blurs the input field. In addition, the increment and decrement buttons will be disabled when the value is
within one `step` value from the bounds ([see below](#step-values) for info about steps). Ranges can be open ended by only
providing either `minValue` or `maxValue` rather than both.

If a valid range is known ahead of time, it is a good idea to provide it to `NumberField` so it can optimize the experience.
For example, when the minimum value is greater than or equal to zero, it is possible to use a numeric keyboard on iOS rather
than a full text keyboard (necessary to enter a minus sign).

```
<NumberField
  label="Enter your age"
  minValue={0} />
```

```
<NumberField
  label="Enter your age"
  minValue={0} />
```

```
<NumberField
  label="Enter your age"
  minValue={0} />
```

### Step values[#](#step-values)

The `step` prop can be used to snap the value to certain increments. If there is a `minValue` defined, the steps are calculated
starting from the minimum. For example, if `minValue={2}`, and `step={3}`, the valid step values would be 2, 5, 8, 11, etc. If no
`minValue` is defined, the steps are calculated starting from zero and extending in both directions. In other words, such that the
values are evenly divisible by the step. If no `step` is defined, any decimal value may be typed, but incrementing and decrementing
snaps the value to an integer.

If the user types a value that is between two steps and blurs the input, the value will be snapped to the nearest step. When
incrementing or decrementing, the value is snapped to the nearest step that is higher or lower, respectively.
When incrementing or decrementing from an empty field, the value starts at the `minValue` or `maxValue`, respectively, if defined.
Otherwise, the value starts from `0`.

```
<NumberField
  label="Step"
  step={10} />
<NumberField
  label="Step + minValue"
  minValue={2}
  step={3} />
<NumberField
  label="Step + minValue + maxValue"
  minValue={2}
  maxValue={21}
  step={3} />
```

```
<NumberField
  label="Step"
  step={10} />
<NumberField
  label="Step + minValue"
  minValue={2}
  step={3} />
<NumberField
  label="Step + minValue + maxValue"
  minValue={2}
  maxValue={21}
  step={3} />
```

```
<NumberField
  label="Step"
  step={10}
/>
<NumberField
  label="Step + minValue"
  minValue={2}
  step={3}
/>
<NumberField
  label="Step + minValue + maxValue"
  minValue={2}
  maxValue={21}
  step={3}
/>
```

### Disabled and read only[#](#disabled-and-read-only)

The `isDisabled` and `isReadOnly` props can be used prevent the user from editing the value of the number field.
The difference is that `isReadOnly` still allows the input to be focused, while `isDisabled` prevents all user interaction.

```
<NumberField label="Disabled" isDisabled value={25} />
<NumberField label="Read only" isReadOnly value={32} />
```

```
<NumberField label="Disabled" isDisabled value={25} />
<NumberField label="Read only" isReadOnly value={32} />
```

```
<NumberField
  label="Disabled"
  isDisabled
  value={25}
/>
<NumberField
  label="Read only"
  isReadOnly
  value={32}
/>
```

## Internationalization[#](#internationalization)

---

`useNumberField` handles many aspects of internationalization automatically, including formatting and parsing numbers according
to the current locale and numbering system. In addition, the increment and decrement buttons have localized ARIA labels.
You are responsible for localizing the label text passed into the number field.

### RTL[#](#rtl)

In right-to-left languages, the number field should be mirrored. The order of the input and buttons should be flipped, and the input
text should be right aligned instead of left aligned. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `decrementAriaLabel` | `string` | â | A custom aria-label for the decrement button. If not provided, the localized string "Decrement" is used. |
| `incrementAriaLabel` | `string` | â | A custom aria-label for the increment button. If not provided, the localized string "Increment" is used. |
| `isWheelDisabled` | `boolean` | â | Enables or disables changing the value with scroll. |
| `formatOptions` | `Intl.NumberFormatOptions` | â | Formatting options for the value displayed in the number field. This also affects what characters are allowed to be typed by the user. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: number )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `value` | `number` | â | The current value (controlled). |
| `defaultValue` | `number` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `minValue` | `number` | â | The smallest value allowed for the input. |
| `maxValue` | `number` | â | The largest value allowed for the input. |
| `step` | `number` | â | The amount that the input value changes with each increment or decrement "tick". |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `onCopy` | `ClipboardEventHandler<HTMLInputElement>` | â | Handler that is called when the user copies text. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/oncopy). |
| `onCut` | `ClipboardEventHandler<HTMLInputElement>` | â | Handler that is called when the user cuts text. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/oncut). |
| `onPaste` | `ClipboardEventHandler<HTMLInputElement>` | â | Handler that is called when the user pastes text. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/onpaste). |
| `onCompositionStart` | `CompositionEventHandler<HTMLInputElement>` | â | Handler that is called when a text composition system starts a new text composition session. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/compositionstart_event). |
| `onCompositionEnd` | `CompositionEventHandler<HTMLInputElement>` | â | Handler that is called when a text composition system completes or cancels the current text composition session. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/compositionend_event). |
| `onCompositionUpdate` | `CompositionEventHandler<HTMLInputElement>` | â | Handler that is called when a new character is received in the current text composition session. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/compositionupdate_event). |
| `onSelect` | `ReactEventHandler<HTMLInputElement>` | â | Handler that is called when text in the input is selected. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/select_event). |
| `onBeforeInput` | `FormEventHandler<HTMLInputElement>` | â | Handler that is called when the input value is about to be modified. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/beforeinput_event). |
| `onInput` | `FormEventHandler<HTMLInputElement>` | â | Handler that is called when the input value is modified. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event). |

`'valid' |Â 'invalid'`

`string |Â string[]`

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Description |
| --- | --- | --- |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `inputValue` | `string` | The current text value of the input. Updated as the user types, and formatted according to `formatOptions` on blur. |
| `numberValue` | `number` | The currently parsed number value, or NaN if a valid number could not be parsed. Updated based on the `inputValue` as the user types. |
| `defaultNumberValue` | `number` | The default value of the input. |
| `canIncrement` | `boolean` | Whether the current value can be incremented according to the maximum value and step. |
| `canDecrement` | `boolean` | Whether the current value can be decremented according to the minimum value and step. |
| `realtimeValidation` | `ValidationResult` | Realtime validation results, updated as the user edits the value. |
| `displayValidation` | `ValidationResult` | Currently displayed validation results, updated when the user commits their changes. |
| `minValue` | `number` | The minimum value of the number field. |
| `maxValue` | `number` | The maximum value of the number field. |

### Methods

| Method | Description |
| --- | --- |
| `validate( (value: string )): boolean` | Validates a user input string according to the current locale and format options. Values can be partially entered, and may be valid even if they cannot currently be parsed to a number. Can be used to implement validation as a user types. |
| `setInputValue( (val: string )): void` | Sets the current text value of the input. |
| `setNumberValue( (val: number )): void` | Sets the number value. |
| `commit(): void` | Commits the current input value. The value is parsed to a number, clamped according to the minimum and maximum values of the field, and snapped to the nearest step value. This will fire the `onChange` prop with the new value, and if uncontrolled, update the `numberValue`. Typically this is called when the field is blurred. |
| `increment(): void` | Increments the current input value to the next step boundary, and fires `onChange`. |
| `decrement(): void` | Decrements the current input value to the next step boundary, and fires `onChange`. |
| `incrementToMax(): void` | Sets the current value to the `maxValue` if any, and fires `onChange`. |
| `decrementToMin(): void` | Sets the current value to the `minValue` if any, and fires `onChange`. |
| `updateValidation( (result: ValidationResult )): void` | Updates the current validation result. Not displayed to the user until `commitValidation` is called. |
| `resetValidation(): void` | Resets the displayed validation state to valid when the user resets the form. |
| `commitValidation(): void` | Commits the realtime validation so it is displayed to the user. |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label element. |
| `groupProps` | `GroupDOMAttributes` | Props for the group wrapper around the input and stepper buttons. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `incrementButtonProps` | `AriaButtonProps` | Props for the increment button, to be passed to `useButton`. |
| `decrementButtonProps` | `AriaButtonProps` | Props for the decrement button, to be passed to `useButton`. |
| `descriptionProps` | `DOMAttributes` | Props for the number field's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the number field's error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

| Name | Type | Description |
| --- | --- | --- |
| `role` | `'group' |Â 'region' |Â 'presentation'` |  |
| `id` | `string |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isDisabled` | `boolean` | â | Whether the button is disabled. |
| `children` | `ReactNode` | â | The content to display in the button. |
| `onPress` | `( (e: PressEvent )) => void` | â | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | â | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | â | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | â | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `href` | `string` | â | A URL to link to if elementType="a". |
| `target` | `string` | â | The target window for the link. |
| `rel` | `string` | â | The relationship between the linked resource and the current page. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel). |
| `elementType` | `ElementType |Â JSXElementConstructor<any>` | `'button'` | The HTML element or React element used to render the button, e.g. 'div', 'a', or `RouterLink`. |
| `aria-disabled` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the element is disabled to users of assistive technology. |
| `aria-expanded` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the element, or another grouping element it controls, is currently expanded or collapsed. |
| `aria-haspopup` | `boolean |Â 'menu' |Â 'listbox' |Â 'tree' |Â 'grid' |Â 'dialog' |Â 'true' |Â 'false'` | â | Indicates the availability and type of interactive popup element, such as menu or dialog, that can be triggered by an element. |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `aria-pressed` | `boolean |Â 'true' |Â 'false' |Â 'mixed'` | â | Indicates the current "pressed" state of toggle buttons. |
| `aria-current` | `boolean |Â 'true' |Â 'false' |Â 'page' |Â 'step' |Â 'location' |Â 'date' |Â 'time'` | â | Indicates whether this element represents the current item within a container or set of related elements. |
| `type` | `'button' |Â 'submit' |Â 'reset'` | `'button'` | The behavior of the button when used in an HTML form. |
| `preventFocusOnPress` | `boolean` | â | Whether to prevent focus from moving to the button when pressing it.  Caution, this can make the button inaccessible and should only be used when alternative keyboard interaction is provided, such as ComboBox's MenuTrigger or a NumberField's increment/decrement control. |
| `form` | `string` | â | The `<form>` element to associate the button with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button#form). |
| `formAction` | `string` | â | The URL that processes the information submitted by the button. Overrides the action attribute of the button's form owner. |
| `formEncType` | `string` | â | Indicates how to encode the form data that is submitted. |
| `formMethod` | `string` | â | Indicates the HTTP method used to submit the form. |
| `formNoValidate` | `boolean` | â | Indicates that the form is not to be validated when it is submitted. |
| `formTarget` | `string` | â | Overrides the target attribute of the button's form owner. |
| `name` | `string` | â | Submitted as a pair with the button's value as part of the form data. |
| `value` | `string` | â | The value associated with the button's name when it's submitted with the form data. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `type` | `'pressstart' |Â 'pressend' |Â 'pressup' |Â 'press'` | The type of press event being fired. |
| `pointerType` | `PointerType` | The pointer type that triggered the press event. |
| `target` | `Element` | The target element of the press event. |
| `shiftKey` | `boolean` | Whether the shift keyboard modifier was held during the press event. |
| `ctrlKey` | `boolean` | Whether the ctrl keyboard modifier was held during the press event. |
| `metaKey` | `boolean` | Whether the meta keyboard modifier was held during the press event. |
| `altKey` | `boolean` | Whether the alt keyboard modifier was held during the press event. |
| `x` | `number` | X position relative to the target. |
| `y` | `number` | Y position relative to the target. |

### Methods

| Method | Description |
| --- | --- |
| `continuePropagation(): void` | By default, press events stop propagation to parent elements. In cases where a handler decides not to handle a specific event, it can call `continuePropagation()` to allow a parent to handle it. |

`'mouse'
|Â 'pen'
|Â 'touch'
|Â 'keyboard'
|Â 'virtual'`

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

Provides state management for a number field component. Number fields allow users to enter a number,
and increment or decrement the value using stepper buttons.

`useNumberFieldState(
(props: NumberFieldStateOptions
)): NumberFieldState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `locale` | `string` | `'en-US'` | The locale that should be used for parsing. |
| `formatOptions` | `Intl.NumberFormatOptions` | â | Formatting options for the value displayed in the number field. This also affects what characters are allowed to be typed by the user. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: number )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `value` | `number` | â | The current value (controlled). |
| `defaultValue` | `number` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `minValue` | `number` | â | The smallest value allowed for the input. |
| `maxValue` | `number` | â | The largest value allowed for the input. |
| `step` | `number` | â | The amount that the input value changes with each increment or decrement "tick". |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |