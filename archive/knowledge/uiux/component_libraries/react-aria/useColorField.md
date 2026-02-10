# useColorField

Source: https://react-spectrum.adobe.com/react-aria/useColorField.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../ColorField).

# useColorField

Provides the behavior and accessibility implementation for a color field component.
Color fields allow users to enter and adjust a hex color value.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useColorField} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/spinbutton/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/color "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/color "View package")

## API[#](#api)

---

`useColorField(
props: AriaColorFieldProps,
state: ColorFieldState,
ref: RefObject<HTMLInputElement
|Â  |Â null>
): ColorFieldAria`

## Features[#](#features)

---

The [<input type="color">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/color) HTML element
can be used to build a color picker, however it is very inconsistent across browsers and operating systems and consists
of a complete color picker rather than a single field for editing a hex value. `useColorField` helps achieve accessible
color fields that can be styled as needed.

- Support for parsing and formatting a hex color value
- Validates keyboard entry as the user types so that only valid hex characters are accepted
- Supports using the arrow keys to increment and decrement the value
- Exposed to assistive technology as a `textbox` via ARIA
- Visual and ARIA labeling support
- Follows the [spinbutton](https://www.w3.org/WAI/ARIA/apg/patterns/spinbutton/) ARIA pattern
- Works around bugs in VoiceOver with the spinbutton role
- Uses an ARIA live region to ensure that value changes are announced

## Anatomy[#](#anatomy)

---

A color field consists of an input element and a label. `useColorField` automatically manages
the relationship between the two elements using the `for` attribute on the `<label>` element
and the `aria-labelledby` attribute on the `<input>` element.

`useColorField` returns two sets of props that you should spread onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `descriptionProps` | `DOMAttributes` | Props for the text field's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the text field's error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

State is managed by the `useColorFieldState`
hook from `@react-stately/color`. The state object should be passed as an option to `useColorField`

If there is no visual label, an `aria-label` or `aria-labelledby` prop must be passed instead
to identify the element to screen readers.

## Example[#](#example)

---

```
import {useColorFieldState} from 'react-stately';
import {useColorField} from 'react-aria';

function ColorField(props) {
  let state = useColorFieldState(props);
  let inputRef = React.useRef(null);
  let {
    labelProps,
    inputProps
  } = useColorField(props, state, inputRef);

  return (
    <div style={{ display: 'inline-flex', flexDirection: 'column' }}>
      <label {...labelProps}>{props.label}</label>
      <input {...inputProps} ref={inputRef} />
    </div>
  );
}

<ColorField label="Color" />
```

```
import {useColorFieldState} from 'react-stately';
import {useColorField} from 'react-aria';

function ColorField(props) {
  let state = useColorFieldState(props);
  let inputRef = React.useRef(null);
  let {
    labelProps,
    inputProps
  } = useColorField(props, state, inputRef);

  return (
    <div
      style={{
        display: 'inline-flex',
        flexDirection: 'column'
      }}
    >
      <label {...labelProps}>{props.label}</label>
      <input {...inputProps} ref={inputRef} />
    </div>
  );
}

<ColorField label="Color" />
```

```
import {useColorFieldState} from 'react-stately';
import {useColorField} from 'react-aria';

function ColorField(
  props
) {
  let state =
    useColorFieldState(
      props
    );
  let inputRef = React
    .useRef(null);
  let {
    labelProps,
    inputProps
  } = useColorField(
    props,
    state,
    inputRef
  );

  return (
    <div
      style={{
        display:
          'inline-flex',
        flexDirection:
          'column'
      }}
    >
      <label
        {...labelProps}
      >
        {props.label}
      </label>
      <input
        {...inputProps}
        ref={inputRef}
      />
    </div>
  );
}

<ColorField label="Color" />
```

## Usage[#](#usage)

---

The following examples show how to use the `ColorField` component created in the above example.

### Uncontrolled[#](#uncontrolled)

By default, `ColorField` is uncontrolled. You can set a default value using the `defaultValue` prop.

```
<ColorField aria-label="Color" defaultValue="#7f007f" />
```

```
<ColorField aria-label="Color" defaultValue="#7f007f" />
```

```
<ColorField
  aria-label="Color"
  defaultValue="#7f007f"
/>
```

### Controlled[#](#controlled)

A `ColorField` can be made controlled. The `parseColor`
function is used to parse the initial color from a hex string, stored in state. The `value` and `onChange` props
are used to update the value in state when the edits the value.

```
import {parseColor} from 'react-stately';

function Example() {
  let [color, setColor] = React.useState(parseColor('#7f007f'));
  return (
    <>
      <ColorField aria-label="Color" value={color} onChange={setColor} />
      <p>Current color value: {color.toString('hex')}</p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [color, setColor] = React.useState(
    parseColor('#7f007f')
  );
  return (
    <>
      <ColorField
        aria-label="Color"
        value={color}
        onChange={setColor}
      />
      <p>Current color value: {color.toString('hex')}</p>
    </>
  );
}
```

```
import {parseColor} from 'react-stately';

function Example() {
  let [color, setColor] =
    React.useState(
      parseColor(
        '#7f007f'
      )
    );
  return (
    <>
      <ColorField
        aria-label="Color"
        value={color}
        onChange={setColor}
      />
      <p>
        Current color
        value:{' '}
        {color.toString(
          'hex'
        )}
      </p>
    </>
  );
}
```

### Disabled and read only[#](#disabled-and-read-only)

A `ColorField` can be disabled using the `isDisabled` prop, and made read only using the `isReadOnly` prop.
The difference is that read only color fields are focusable but disabled color fields are not.

```
<ColorField aria-label="Color" defaultValue="#7f007f" isDisabled />
<ColorField aria-label="Color" defaultValue="#7f007f" isReadOnly />
```

```
<ColorField
  aria-label="Color"
  defaultValue="#7f007f"
  isDisabled
/>
<ColorField
  aria-label="Color"
  defaultValue="#7f007f"
  isReadOnly
/>
```

```
<ColorField
  aria-label="Color"
  defaultValue="#7f007f"
  isDisabled
/>
<ColorField
  aria-label="Color"
  defaultValue="#7f007f"
  isReadOnly
/>
```

### HTML forms[#](#html-forms)

ColorField supports the `name` prop for integration with HTML forms. The value will be submitted to the server as a hex color string.

```
<ColorField label="Color" name="color" />
```

```
<ColorField label="Color" name="color" />
```

```
<ColorField
  label="Color"
  name="color"
/>
```

## Internationalization[#](#internationalization)

---

### RTL[#](#rtl)

In right-to-left languages, color fields should be mirrored. The label should be right aligned,
along with the text in the input. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isWheelDisabled` | `boolean` | â | Enables or disables changing the value with scroll. |
| `onChange` | `( (color: Color |Â  |Â null )) => void` | â | Handler that is called when the value changes. |
| `value` | `T` | â | The current value (controlled). |
| `defaultValue` | `T` | â | The default value (uncontrolled). |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: Color |Â  |Â null )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `onCopy` | `ClipboardEventHandler<HTMLInputElement>` | â | Handler that is called when the user copies text. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/oncopy). |
| `onCut` | `ClipboardEventHandler<HTMLInputElement>` | â | Handler that is called when the user cuts text. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/oncut). |
| `onPaste` | `ClipboardEventHandler<HTMLInputElement>` | â | Handler that is called when the user pastes text. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/onpaste). |
| `onCompositionStart` | `CompositionEventHandler<HTMLInputElement>` | â | Handler that is called when a text composition system starts a new text composition session. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/compositionstart_event). |
| `onCompositionEnd` | `CompositionEventHandler<HTMLInputElement>` | â | Handler that is called when a text composition system completes or cancels the current text composition session. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/compositionend_event). |
| `onCompositionUpdate` | `CompositionEventHandler<HTMLInputElement>` | â | Handler that is called when a new character is received in the current text composition session. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/compositionupdate_event). |
| `onSelect` | `ReactEventHandler<HTMLInputElement>` | â | Handler that is called when text in the input is selected. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/select_event). |
| `onBeforeInput` | `FormEventHandler<HTMLInputElement>` | â | Handler that is called when the input value is about to be modified. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/beforeinput_event). |
| `onInput` | `FormEventHandler<HTMLInputElement>` | â | Handler that is called when the input value is modified. See [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event). |
| `aria-errormessage` | `string` | â | Identifies the element that provides an error message for the object. |

Represents a color value.

| Method | Description |
| --- | --- |
| `toFormat( (format: ColorFormat )): Color` | Converts the color to the given color format, and returns a new Color object. |
| `toString( (format?: ColorFormat |Â  |Â 'css' )): string` | Converts the color to a string in the given format. |
| `clone(): Color` | Returns a duplicate of the color value. |
| `toHexInt(): number` | Converts the color to hex, and returns an integer representation. |
| `getChannelValue( (channel: ColorChannel )): number` | Returns the numeric value for a given channel. Throws an error if the channel is unsupported in the current color format. |
| `withChannelValue( (channel: ColorChannel, , value: number )): Color` | Sets the numeric value for a given channel, and returns a new Color object. Throws an error if the channel is unsupported in the current color format. |
| `getChannelRange( (channel: ColorChannel )): ColorChannelRange` | Returns the minimum, maximum, and step values for a given channel. |
| `getChannelName( (channel: ColorChannel, , locale: string )): string` | Returns a localized color channel name for a given channel and locale, for use in visual or accessibility labels. |
| `getChannelFormatOptions( (channel: ColorChannel )): Intl.NumberFormatOptions` | Returns the number formatting options for the given channel. |
| `formatChannelValue( (channel: ColorChannel, , locale: string )): string` | Formats the numeric value for a given channel for display according to the provided locale. |
| `getColorSpace(): ColorSpace` | Returns the color space, 'rgb', 'hsb' or 'hsl', for the current color. |
| `getColorSpaceAxes( (xyChannels: { xChannel?: ColorChannel,  yChannel?: ColorChannel } )): ColorAxes` | Returns the color space axes, xChannel, yChannel, zChannel. |
| `getColorChannels(): [ ColorChannel, ColorChannel, ColorChannel ]` | Returns an array of the color channels within the current color space space. |
| `getColorName( (locale: string )): string` | Returns a localized name for the color, for use in visual or accessibility labels. |
| `getHueName( (locale: string )): string` | Returns a localized name for the hue, for use in visual or accessibility labels. |

A list of supported color formats.

`'hex'
|Â 'hexa'
|Â 'rgb'
|Â 'rgba'
|Â 'hsl'
|Â 'hsla'
|Â 'hsb'
|Â 'hsba'`

A list of color channels.

`'hue'
|Â 'saturation'
|Â 'brightness'
|Â 'lightness'
|Â 'red'
|Â 'green'
|Â 'blue'
|Â 'alpha'`

| Name | Type | Description |
| --- | --- | --- |
| `minValue` | `number` | The minimum value of the color channel. |
| `maxValue` | `number` | The maximum value of the color channel. |
| `step` | `number` | The step value of the color channel, used when incrementing and decrementing. |
| `pageSize` | `number` | The page step value of the color channel, used when incrementing and decrementing. |

`'rgb'
|Â 'hsl'
|Â 'hsb'`

`{

xChannel: ColorChannel,

yChannel: ColorChannel,

zChannel: ColorChannel

}`

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
| `colorValue` | `Color |Â null` | The currently parsed color value, or null if the field is empty. Updated based on the `inputValue` as the user types. |
| `defaultColorValue` | `Color |Â null` | The default value of the color field. |
| `realtimeValidation` | `ValidationResult` | Realtime validation results, updated as the user edits the value. |
| `displayValidation` | `ValidationResult` | Currently displayed validation results, updated when the user commits their changes. |

### Methods

| Method | Description |
| --- | --- |
| `setColorValue( (value: Color |Â  |Â null )): void` | Sets the color value of the field. |
| `setInputValue( (value: string )): void` | Sets the current text value of the input. |
| `commit(): void` | Updates the input value based on the currently parsed color value. Typically this is called when the field is blurred. |
| `increment(): void` | Increments the current input value to the next step boundary, and fires `onChange`. |
| `decrement(): void` | Decrements the current input value to the next step boundary, and fires `onChange`. |
| `incrementToMax(): void` | Sets the current value to the maximum color value, and fires `onChange`. |
| `decrementToMin(): void` | Sets the current value to the minimum color value, and fires `onChange`. |
| `validate( (value: string )): boolean` | Validates a user input string. Values can be partially entered, and may be valid even if they cannot currently be parsed to a color. Can be used to implement validation as a user types. |
| `updateValidation( (result: ValidationResult )): void` | Updates the current validation result. Not displayed to the user until `commitValidation` is called. |
| `resetValidation(): void` | Resets the displayed validation state to valid when the user resets the form. |
| `commitValidation(): void` | Commits the realtime validation so it is displayed to the user. |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `descriptionProps` | `DOMAttributes` | Props for the text field's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the text field's error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`

Provides state management for a color field component. Color fields allow
users to enter and adjust a hex color value.

`useColorFieldState(
(props: ColorFieldProps
)): ColorFieldState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `onChange` | `( (color: Color |Â  |Â null )) => void` | â | Handler that is called when the value changes. |
| `value` | `T` | â | The current value (controlled). |
| `defaultValue` | `T` | â | The default value (uncontrolled). |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: Color |Â  |Â null )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |

Parses a color from a string value. Throws an error if the string could not be parsed.

`parseColor(
(value: string
)): Color`