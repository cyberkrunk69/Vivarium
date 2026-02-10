# useTextField

Source: https://react-spectrum.adobe.com/react-aria/useTextField.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../TextField).

# useTextField

Provides the behavior and accessibility implementation for a text field.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useTextField} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/TR/wai-aria-1.2/#textbox "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/textfield "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/textfield "View package")

## API[#](#api)

---

`useTextField<T extends TextFieldIntrinsicElements = DefaultElementType>(
(props: AriaTextFieldOptions<T>,
, ref: TextFieldRefObject<T>
)): TextFieldAria<T>`

## Features[#](#features)

---

Text fields can be built with [<input>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input)
or [<textarea>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea)
and [<label>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label) elements,
but you must manually ensure that they are semantically connected via ids for accessibility.
`useTextField` helps automate this, and handle other accessibility features while
allowing for custom styling.

- Built with a native `<input>` or `<textarea>` element
- Visual and ARIA labeling support
- Change, clipboard, composition, selection, and input event support
- Support for native HTML constraint validation with customizable UI, custom validation functions, realtime validation, and server-side validation errors
- Support for description and error message help text linked to the input via ARIA

## Anatomy[#](#anatomy)

---

Text fields consist of an input element and a label. `useTextField` automatically manages
the relationship between the two elements using the `for` attribute on the `<label>` element
and the `aria-labelledby` attribute on the `<input>` element.

`useTextField` also supports optional description and error message elements, which can be used
to provide more context about the field, and any validation messages. These are linked with the
input via the `aria-describedby` attribute.

`useTextField` returns props that you should spread onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `inputProps` | `TextFieldInputProps<TextFieldIntrinsicElements>` | Props for the input element. |
| `labelProps` | `DOMAttributes |Â LabelHTMLAttributes<HTMLLabelElement>` | Props for the text field's visible label element, if any. |
| `descriptionProps` | `DOMAttributes` | Props for the text field's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the text field's error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

If there is no visual label, an `aria-label` or `aria-labelledby` prop must be passed instead
to identify the element to screen readers.

## Example[#](#example)

---

```
import type {AriaTextFieldProps} from 'react-aria';
import {useTextField} from 'react-aria';

function TextField(props: AriaTextFieldProps) {
  let { label } = props;
  let ref = React.useRef(null);
  let {
    labelProps,
    inputProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useTextField(props, ref);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: 200 }}>
      <label {...labelProps}>{label}</label>
      <input {...inputProps} ref={ref} />
      {props.description && (
        <div {...descriptionProps} style={{ fontSize: 12 }}>
          {props.description}
        </div>
      )}
      {isInvalid && (
        <div {...errorMessageProps} style={{ color: 'red', fontSize: 12 }}>
          {validationErrors.join(' ')}
        </div>
      )}
    </div>
  );
}

<TextField label="Email" />
```

```
import type {AriaTextFieldProps} from 'react-aria';
import {useTextField} from 'react-aria';

function TextField(props: AriaTextFieldProps) {
  let { label } = props;
  let ref = React.useRef(null);
  let {
    labelProps,
    inputProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useTextField(props, ref);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        width: 200
      }}
    >
      <label {...labelProps}>{label}</label>
      <input {...inputProps} ref={ref} />
      {props.description && (
        <div {...descriptionProps} style={{ fontSize: 12 }}>
          {props.description}
        </div>
      )}
      {isInvalid && (
        <div
          {...errorMessageProps}
          style={{ color: 'red', fontSize: 12 }}
        >
          {validationErrors.join(' ')}
        </div>
      )}
    </div>
  );
}

<TextField label="Email" />
```

```
import type {AriaTextFieldProps} from 'react-aria';
import {useTextField} from 'react-aria';

function TextField(
  props:
    AriaTextFieldProps
) {
  let { label } = props;
  let ref = React.useRef(
    null
  );
  let {
    labelProps,
    inputProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useTextField(
    props,
    ref
  );

  return (
    <div
      style={{
        display: 'flex',
        flexDirection:
          'column',
        width: 200
      }}
    >
      <label
        {...labelProps}
      >
        {label}
      </label>
      <input
        {...inputProps}
        ref={ref}
      />
      {props
        .description && (
        <div
          {...descriptionProps}
          style={{
            fontSize: 12
          }}
        >
          {props
            .description}
        </div>
      )}
      {isInvalid && (
        <div
          {...errorMessageProps}
          style={{
            color: 'red',
            fontSize: 12
          }}
        >
          {validationErrors
            .join(' ')}
        </div>
      )}
    </div>
  );
}

<TextField label="Email" />
```

### Text area[#](#text-area)

`useTextField` also supports multi-line text entry with the `<textarea>` element via the `inputElementType` prop.

```
import type {AriaTextFieldProps} from 'react-aria';
import {useTextField} from 'react-aria';

function TextArea(props: AriaTextFieldProps<HTMLTextAreaElement>) {
  let { label } = props;
  let ref = React.useRef(null);
  let { labelProps, inputProps } = useTextField({
    ...props,
    inputElementType: 'textarea'
  }, ref);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: 200 }}>
      <label {...labelProps}>{label}</label>
      <textarea {...inputProps} ref={ref} />
    </div>
  );
}

<TextArea label="Description" />
```

```
import type {AriaTextFieldProps} from 'react-aria';
import {useTextField} from 'react-aria';

function TextArea(
  props: AriaTextFieldProps<HTMLTextAreaElement>
) {
  let { label } = props;
  let ref = React.useRef(null);
  let { labelProps, inputProps } = useTextField({
    ...props,
    inputElementType: 'textarea'
  }, ref);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        width: 200
      }}
    >
      <label {...labelProps}>{label}</label>
      <textarea {...inputProps} ref={ref} />
    </div>
  );
}

<TextArea label="Description" />
```

```
import type {AriaTextFieldProps} from 'react-aria';
import {useTextField} from 'react-aria';

function TextArea(
  props:
    AriaTextFieldProps<
      HTMLTextAreaElement
    >
) {
  let { label } = props;
  let ref = React.useRef(
    null
  );
  let {
    labelProps,
    inputProps
  } = useTextField({
    ...props,
    inputElementType:
      'textarea'
  }, ref);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection:
          'column',
        width: 200
      }}
    >
      <label
        {...labelProps}
      >
        {label}
      </label>
      <textarea
        {...inputProps}
        ref={ref}
      />
    </div>
  );
}

<TextArea label="Description" />
```

## Usage[#](#usage)

---

The following examples show how to use the `TextField` component created in the above example.

### Default value[#](#default-value)

A TextField's `value` is empty by default, but an initial, uncontrolled, value can be provided using the `defaultValue` prop.

```
<TextField
  label="Email"
  defaultValue="me@email.com" />
```

```
<TextField
  label="Email"
  defaultValue="me@email.com" />
```

```
<TextField
  label="Email"
  defaultValue="me@email.com"
/>
```

### Controlled value[#](#controlled-value)

The `value` prop can be used to make the value controlled. The `onChange` event is fired when the user edits the text, and receives the new value.

```
function Example() {
  let [text, setText] = React.useState('');

  return (
    <>
      <TextField label="Your text" onChange={setText} />
      <p>Mirrored text: {text}</p>
    </>
  );
}
```

```
function Example() {
  let [text, setText] = React.useState('');

  return (
    <>
      <TextField label="Your text" onChange={setText} />
      <p>Mirrored text: {text}</p>
    </>
  );
}
```

```
function Example() {
  let [text, setText] =
    React.useState('');

  return (
    <>
      <TextField
        label="Your text"
        onChange={setText}
      />
      <p>
        Mirrored text:
        {' '}
        {text}
      </p>
    </>
  );
}
```

### Description[#](#description)

The `description` prop can be used to associate additional help text with a text field.

```
<TextField
  label="Email"
  description="Enter an email for us to contact you about your order."
/>
```

```
<TextField
  label="Email"
  description="Enter an email for us to contact you about your order."
/>
```

```
<TextField
  label="Email"
  description="Enter an email for us to contact you about your order."
/>
```

### Validation[#](#validation)

useTextField supports HTML constraint validation props such as `isRequired`, `type="email"`, `minLength`, and `pattern`, as well as custom validation functions, realtime validation, and server-side validation. It can also be integrated with other form libraries. See the [Forms](../forms) guide to learn more.

When a TextField has the `validationBehavior="native"` prop, validation errors block form submission. To display validation errors, use the `validationErrors` and `errorMessageProps` returned by `useTextField`. This allows you to render error messages from all of the above sources with consistent custom styles.

```
<form>
  <TextField
    label="Email"
    name="email"
    type="email"
    isRequired
    validationBehavior="native"  />
  <input type="submit" style={{marginTop: 8}} />
</form>
```

```
<form>
  <TextField
    label="Email"
    name="email"
    type="email"
    isRequired
    validationBehavior="native"  />
  <input type="submit" style={{marginTop: 8}} />
</form>
```

```
<form>
  <TextField
    label="Email"
    name="email"
    type="email"
    isRequired
    validationBehavior="native"  />
  <input
    type="submit"
    style={{
      marginTop: 8
    }}
  />
</form>
```

### Disabled[#](#disabled)

A TextField can be disabled using the `isDisabled` prop.

```
<TextField label="Email" isDisabled />
```

```
<TextField label="Email" isDisabled />
```

```
<TextField
  label="Email"
  isDisabled
/>
```

### Read only[#](#read-only)

The `isReadOnly` boolean prop makes the TextField's text content immutable. Unlike `isDisabled`, the TextField remains focusable
and the contents can still be copied. See [the MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/readonly) for more information.

```
<TextField label="Email" defaultValue="abc@adobe.com" isReadOnly />
```

```
<TextField
  label="Email"
  defaultValue="abc@adobe.com"
  isReadOnly
/>
```

```
<TextField
  label="Email"
  defaultValue="abc@adobe.com"
  isReadOnly
/>
```

### Required[#](#required)

A TextField can be marked as required using the `isRequired` prop. This is exposed to assistive technologies by React Aria. It's your responsibility to add additional visual styling if needed.

```
<TextField label="Email" isRequired />
```

```
<TextField label="Email" isRequired />
```

```
<TextField
  label="Email"
  isRequired
/>
```

### HTML forms[#](#html-forms)

TextField supports the `name` prop for integration with HTML forms. In addition, attributes such as `type`, `pattern`, `inputMode`, and others are passed through to the underlying `<input>` element.

```
<TextField label="Email" name="email" type="email" />
```

```
<TextField label="Email" name="email" type="email" />
```

```
<TextField
  label="Email"
  name="email"
  type="email"
/>
```

## Internationalization[#](#internationalization)

---

### RTL[#](#rtl)

In right-to-left languages, text fields should be mirrored. The label should be right aligned,
along with the text in the text field. Ensure that your CSS accounts for this.

The intrinsic HTML element names that `useTextField` supports; e.g. `input`,
`textarea`.

`keyof <IntrinsicHTMLElements, 'input' |Â 'textarea'>`

A map of HTML element names and their interface types.
For example `'a'` -> `HTMLAnchorElement`.

`'input'`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `inputElementType` | `TextFieldIntrinsicElements` | `'input'` | The HTML element used to render the input, e.g. 'input', or 'textarea'. It determines whether certain HTML attributes will be included in `inputProps`. For example, [`type`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#attr-type). |
| `autoCapitalize` | `'off' |Â 'none' |Â 'on' |Â 'sentences' |Â 'words' |Â 'characters'` | â | Controls whether inputted text is automatically capitalized and, if so, in what manner. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/autocapitalize). |
| `enterKeyHint` | `'enter' |Â 'done' |Â 'go' |Â 'next' |Â 'previous' |Â 'search' |Â 'send'` | â | An enumerated attribute that defines what action label or icon to preset for the enter key on virtual keyboards. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/enterkeyhint). |
| `aria-activedescendant` | `string` | â | Identifies the currently active element when DOM focus is on a composite widget, textbox, group, or application. |
| `aria-autocomplete` | `'none' |Â 'inline' |Â 'list' |Â 'both'` | â | Indicates whether inputting text could trigger display of one or more predictions of the user's intended value for an input and specifies how predictions would be presented if they are made. |
| `aria-haspopup` | `boolean |Â 'false' |Â 'true' |Â 'menu' |Â 'listbox' |Â 'tree' |Â 'grid' |Â 'dialog'` | â | Indicates the availability and type of interactive popup element, such as menu or dialog, that can be triggered by an element. |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: string )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<TextFieldHTMLElementType[TextFieldIntrinsicElements]> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<TextFieldHTMLElementType[TextFieldIntrinsicElements]> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `value` | `string` | â | The current value (controlled). |
| `defaultValue` | `string` | â | The default value (uncontrolled). |
| `onChange` | `( (value: TextFieldHTMLElementType[TextFieldIntrinsicElements] )) => void` | â | Handler that is called when the value changes. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `autoComplete` | `string` | â | Describes the type of autocomplete functionality the input should provide if any. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefautocomplete). |
| `maxLength` | `number` | â | The maximum number of characters supported by the input. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefmaxlength). |
| `minLength` | `number` | â | The minimum number of characters required by the input. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefminlength). |
| `pattern` | `string` | â | Regex pattern that the value of the input must match to be valid. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefpattern). |
| `type` | `'text' |Â 'search' |Â 'url' |Â 'tel' |Â 'email' |Â 'password' |Â string &Â  &Â {}` | `'text'` | The type of input to render. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdeftype). |
| `inputMode` | `'none' |Â 'text' |Â 'tel' |Â 'url' |Â 'email' |Â 'numeric' |Â 'decimal' |Â 'search'` | â | Hints at the type of data that might be entered by the user while editing the element or its contents. See [MDN](https://html.spec.whatwg.org/multipage/interaction.html#input-modalities:-the-inputmode-attribute). |
| `autoCorrect` | `string` | â | An attribute that takes as its value a space-separated string that describes what, if any, type of autocomplete functionality the input should provide. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#autocomplete). |
| `spellCheck` | `string` | â | An enumerated attribute that defines whether the element may be checked for spelling errors. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/spellcheck). |
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

`'valid' |Â 'invalid'`

`string |Â string[]`

| Name | Type | Description |
| --- | --- | --- |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

The HTML element interfaces that `useTextField` supports based on what is
defined for `TextFieldIntrinsicElements`; e.g. `HTMLInputElement`,
`HTMLTextAreaElement`.

`<IntrinsicHTMLElements, TextFieldIntrinsicElements>`

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

The type of `ref` object that can be passed to `useTextField` based on the given
intrinsic HTML element name; e.g.`RefObject<HTMLInputElement>`,
`RefObject<HTMLTextAreaElement>`.

`RefObject<TextFieldHTMLElementType[T] |Â null>`

| Name | Type | Description |
| --- | --- | --- |
| `inputProps` | `TextFieldInputProps<TextFieldIntrinsicElements>` | Props for the input element. |
| `labelProps` | `DOMAttributes |Â LabelHTMLAttributes<HTMLLabelElement>` | Props for the text field's visible label element, if any. |
| `descriptionProps` | `DOMAttributes` | Props for the text field's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the text field's error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

The type of `inputProps` returned by `useTextField`; e.g. `InputHTMLAttributes`,
`TextareaHTMLAttributes`.

`TextFieldHTMLAttributesType[TextFieldIntrinsicElements]`

The HTML attributes interfaces that `useTextField` supports based on what
is defined for `TextFieldIntrinsicElements`; e.g. `InputHTMLAttributes`,
`TextareaHTMLAttributes`.

`JSX.IntrinsicElements<IntrinsicHTMLAttributes, TextFieldIntrinsicElements>`

A map of HTML element names and their attribute interface types.
For example `'a'` -> `AnchorHTMLAttributes<HTMLAnchorElement>`.

`JSX.IntrinsicElements`

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