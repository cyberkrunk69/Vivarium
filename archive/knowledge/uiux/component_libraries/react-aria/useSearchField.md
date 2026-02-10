# useSearchField

Source: https://react-spectrum.adobe.com/react-aria/useSearchField.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../SearchField).

# useSearchField

Provides the behavior and accessibility implementation for a search field.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useSearchField} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/TR/wai-aria-1.2/#searchbox "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/searchfield "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/searchfield "View package")

## API[#](#api)

---

`useSearchField(
props: AriaSearchFieldProps,
state: SearchFieldState,
inputRef: RefObject<HTMLInputElement
|Â  |Â null>
): SearchFieldAria`

## Features[#](#features)

---

Search fields can be built with `<input type="search">`, but these can be hard to
style consistently cross browser. `useSearchField` helps achieve accessible
search fields that can be styled as needed.

- Built with a native `<input type="search">` element
- Visual and ARIA labeling support
- Keyboard submit handling via the `Enter` key
- Keyboard support for clearing the search field with the `Escape` key
- Custom clear button support with internationalized label for accessibility
- Support for native HTML constraint validation with customizable UI, custom validation functions, realtime validation, and server-side validation errors

## Anatomy[#](#anatomy)

---

Search fields consist of an input element, a label, and an optional clear button.
`useSearchField` automatically manages the labeling and relationships between the elements,
and handles keyboard events. Users can press the `Escape` key to clear the search field, or
the `Enter` key to trigger the `onSubmit` event.

`useSearchField` also supports optional description and error message elements, which can be used
to provide more context about the field, and any validation messages. These are linked with the
input via the `aria-describedby` attribute.

`useSearchField` returns props that you should spread onto the appropriate elements:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the text field's visible label element (if any). |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `clearButtonProps` | `AriaButtonProps` | Props for the clear button. |
| `descriptionProps` | `DOMAttributes` | Props for the searchfield's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the searchfield's error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

State is managed by the `useSearchFieldState`
hook in `@react-stately/searchfield`. The state object should be passed as an option to `useSearchField`.

If there is no visual label, an `aria-label` or `aria-labelledby` prop must be passed instead
to identify the element to screen readers.

## Example[#](#example)

---

**Note**: This example does not show the optional description or error message elements. See [useTextField](../TextField/useTextField.html) for an example of that.

```
import {useSearchFieldState} from 'react-stately';
import {useSearchField} from 'react-aria';

function SearchField(props) {
  let { label } = props;
  let state = useSearchFieldState(props);
  let ref = React.useRef(null);
  let { labelProps, inputProps } = useSearchField(props, state, ref);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: 200 }}>
      <label {...labelProps}>{label}</label>
      <input {...inputProps} ref={ref} />
    </div>
  );
}

<SearchField
  label="Search"
  onSubmit={(text) => alert(text)}
/>
```

```
import {useSearchFieldState} from 'react-stately';
import {useSearchField} from 'react-aria';

function SearchField(props) {
  let { label } = props;
  let state = useSearchFieldState(props);
  let ref = React.useRef(null);
  let { labelProps, inputProps } = useSearchField(
    props,
    state,
    ref
  );

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
    </div>
  );
}

<SearchField
  label="Search"
  onSubmit={(text) => alert(text)}
/>
```

```
import {useSearchFieldState} from 'react-stately';
import {useSearchField} from 'react-aria';

function SearchField(
  props
) {
  let { label } = props;
  let state =
    useSearchFieldState(
      props
    );
  let ref = React.useRef(
    null
  );
  let {
    labelProps,
    inputProps
  } = useSearchField(
    props,
    state,
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
    </div>
  );
}

<SearchField
  label="Search"
  onSubmit={(text) =>
    alert(text)}
/>
```

## Styling[#](#styling)

---

This example uses CSS to reset the default browser styling for a search field and implement
custom styles. It also includes a custom clear button, built with [useButton](../Button/useButton.html).
The `Button` component is independent, and can be shared with many other components.

```
// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function SearchField(props) {
  let { label } = props;
  let state = useSearchFieldState(props);
  let ref = React.useRef(null);
  let { labelProps, inputProps, clearButtonProps } = useSearchField(
    props,
    state,
    ref
  );

  return (
    <div className="search-field">
      <label {...labelProps}>{label}</label>
      <div>
        <input {...inputProps} ref={ref} />
        {state.value !== '' &&
          <Button {...clearButtonProps}>â</Button>}
      </div>
    </div>
  );
}

<SearchField
  label="Search"
  onSubmit={(text) => alert(text)}
/>
```

```
// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function SearchField(props) {
  let { label } = props;
  let state = useSearchFieldState(props);
  let ref = React.useRef(null);
  let { labelProps, inputProps, clearButtonProps } =
    useSearchField(props, state, ref);

  return (
    <div className="search-field">
      <label {...labelProps}>{label}</label>
      <div>
        <input {...inputProps} ref={ref} />
        {state.value !== '' &&
          <Button {...clearButtonProps}>â</Button>}
      </div>
    </div>
  );
}

<SearchField
  label="Search"
  onSubmit={(text) => alert(text)}
/>
```

```
// Reuse the Button from your component library. See below for details.
import {Button} from 'your-component-library';

function SearchField(
  props
) {
  let { label } = props;
  let state =
    useSearchFieldState(
      props
    );
  let ref = React.useRef(
    null
  );
  let {
    labelProps,
    inputProps,
    clearButtonProps
  } = useSearchField(
    props,
    state,
    ref
  );

  return (
    <div className="search-field">
      <label
        {...labelProps}
      >
        {label}
      </label>
      <div>
        <input
          {...inputProps}
          ref={ref}
        />
        {state.value !==
            '' &&
          (
            <Button
              {...clearButtonProps}
            >
              â
            </Button>
          )}
      </div>
    </div>
  );
}

<SearchField
  label="Search"
  onSubmit={(text) =>
    alert(text)}
/>
```

 Show CSS

```
/* css */
.search-field {
  display: flex;
  flex-direction: column;
}

.search-field div {
  background: slategray;
  padding: 4px 0 4px 4px;
  border-radius: 4px;
  width: 250px;
  display: flex;
}

.search-field input {
  flex: 1;
  color: white;
  font-size: 15px;
  padding: 2px 0;
}

.search-field input, .search-field button {
  -webkit-appearance: none;
  border: none;
  outline: none;
  background: none;
}

.search-field input::-webkit-search-cancel-button,
.search-field input::-webkit-search-decoration {
  -webkit-appearance: none;
}
```

```
/* css */
.search-field {
  display: flex;
  flex-direction: column;
}

.search-field div {
  background: slategray;
  padding: 4px 0 4px 4px;
  border-radius: 4px;
  width: 250px;
  display: flex;
}

.search-field input {
  flex: 1;
  color: white;
  font-size: 15px;
  padding: 2px 0;
}

.search-field input, .search-field button {
  -webkit-appearance: none;
  border: none;
  outline: none;
  background: none;
}

.search-field input::-webkit-search-cancel-button,
.search-field input::-webkit-search-decoration {
  -webkit-appearance: none;
}
```

```
/* css */
.search-field {
  display: flex;
  flex-direction: column;
}

.search-field div {
  background: slategray;
  padding: 4px 0 4px 4px;
  border-radius: 4px;
  width: 250px;
  display: flex;
}

.search-field input {
  flex: 1;
  color: white;
  font-size: 15px;
  padding: 2px 0;
}

.search-field input, .search-field button {
  -webkit-appearance: none;
  border: none;
  outline: none;
  background: none;
}

.search-field input::-webkit-search-cancel-button,
.search-field input::-webkit-search-decoration {
  -webkit-appearance: none;
}
```

### Button[#](#button)

The `Button` component is used in the above example to clear the search field. It is built using the [useButton](../Button/useButton.html) hook, and can be shared with many other components.

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

The following examples show how to use the `SearchField` component created in the above example.

### Default value[#](#default-value)

A SearchField's `value` is empty by default, but an initial, uncontrolled, value can be provided using the `defaultValue` prop.

```
<SearchField
  label="Search"
  defaultValue="Puppies" />
```

```
<SearchField
  label="Search"
  defaultValue="Puppies" />
```

```
<SearchField
  label="Search"
  defaultValue="Puppies"
/>
```

### Controlled value[#](#controlled-value)

The `value` prop can be used to make the value controlled. The `onChange` event is fired when the user edits the text, and receives the new value.

```
function Example() {
  let [text, setText] = React.useState('');

  return (
    <>
      <SearchField label="Search" onChange={setText} />
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
      <SearchField label="Search" onChange={setText} />
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
      <SearchField
        label="Search"
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

### Events[#](#events)

The most commonly used handlers for events in SearchField are the:

- `onChange` prop which is triggered whenever the value is edited by the user.
- `onSubmit` prop which is triggered whenever the value is submitted by the user (e.g. by pressing `Enter`).
- `onClear` prop which is triggered whenever the value is cleared by the user (e.g. by pressing clear button or `Escape` key).

The example below uses `onChange`, `onSubmit`, and `onClear` to update two separate elements with the text entered into the SearchField.

```
function Example() {
  let [currentText, setCurrentText] = React.useState('');
  let [submittedText, setSubmittedText] = React.useState('');

  return (
    <div>
      <SearchField
        onClear={() => setCurrentText('')}
        onChange={setCurrentText}
        onSubmit={setSubmittedText}
        label="Your text"
        value={currentText}
      />
      <p>Mirrored text: {currentText}</p>
      <p>Submitted text: {submittedText}</p>
    </div>
  );
}
```

```
function Example() {
  let [currentText, setCurrentText] = React.useState('');
  let [submittedText, setSubmittedText] = React.useState(
    ''
  );

  return (
    <div>
      <SearchField
        onClear={() => setCurrentText('')}
        onChange={setCurrentText}
        onSubmit={setSubmittedText}
        label="Your text"
        value={currentText}
      />
      <p>Mirrored text: {currentText}</p>
      <p>Submitted text: {submittedText}</p>
    </div>
  );
}
```

```
function Example() {
  let [
    currentText,
    setCurrentText
  ] = React.useState('');
  let [
    submittedText,
    setSubmittedText
  ] = React.useState('');

  return (
    <div>
      <SearchField
        onClear={() =>
          setCurrentText(
            ''
          )}
        onChange={setCurrentText}
        onSubmit={setSubmittedText}
        label="Your text"
        value={currentText}
      />
      <p>
        Mirrored text:
        {' '}
        {currentText}
      </p>
      <p>
        Submitted text:
        {' '}
        {submittedText}
      </p>
    </div>
  );
}
```

### Disabled[#](#disabled)

A SearchField can be disabled using the `isDisabled` prop.

```
<SearchField label="Email" isDisabled />
```

```
<SearchField label="Email" isDisabled />
```

```
<SearchField
  label="Email"
  isDisabled
/>
```

### Read only[#](#read-only)

The `isReadOnly` boolean prop makes the SearchField's text content immutable. Unlike `isDisabled`, the SearchField remains focusable
and the contents can still be copied. See [the MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/readonly) for more information.

```
<SearchField label="Email" defaultValue="abc@adobe.com" isReadOnly />
```

```
<SearchField
  label="Email"
  defaultValue="abc@adobe.com"
  isReadOnly
/>
```

```
<SearchField
  label="Email"
  defaultValue="abc@adobe.com"
  isReadOnly
/>
```

### HTML forms[#](#html-forms)

SearchField supports the `name` prop for integration with HTML forms. In addition, attributes such as `type`, `pattern`, `inputMode`, and others are passed through to the underlying `<input>` element.

```
<SearchField label="Email" name="email" type="email" />
```

```
<SearchField label="Email" name="email" type="email" />
```

```
<SearchField
  label="Email"
  name="email"
  type="email"
/>
```

## Internationalization[#](#internationalization)

---

### RTL[#](#rtl)

In right-to-left languages, search fields should be mirrored. The label should be right aligned,
along with the text in the input. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `enterKeyHint` | `'enter' |Â 'done' |Â 'go' |Â 'next' |Â 'previous' |Â 'search' |Â 'send'` | â | An enumerated attribute that defines what action label or icon to preset for the enter key on virtual keyboards. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/enterkeyhint). |
| `type` | `'text' |Â 'search' |Â 'url' |Â 'tel' |Â 'email' |Â 'password' |Â string &Â  &Â {}` | `'search'` | The type of input to render. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdeftype). |
| `onSubmit` | `( (value: string )) => void` | â | Handler that is called when the SearchField is submitted. |
| `onClear` | `() => void` | â | Handler that is called when the clear button is pressed. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: string )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<T> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<T> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `value` | `string` | â | The current value (controlled). |
| `defaultValue` | `string` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `aria-activedescendant` | `string` | â | Identifies the currently active element when DOM focus is on a composite widget, textbox, group, or application. |
| `aria-autocomplete` | `'none' |Â 'inline' |Â 'list' |Â 'both'` | â | Indicates whether inputting text could trigger display of one or more predictions of the user's intended value for an input and specifies how predictions would be presented if they are made. |
| `aria-haspopup` | `boolean |Â 'false' |Â 'true' |Â 'menu' |Â 'listbox' |Â 'tree' |Â 'grid' |Â 'dialog'` | â | Indicates the availability and type of interactive popup element, such as menu or dialog, that can be triggered by an element. |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
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

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `value` | `string` | The current value of the search field. |

### Methods

| Method | Description |
| --- | --- |
| `setValue( (value: string )): void` | Sets the value of the search field. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the text field's visible label element (if any). |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `clearButtonProps` | `AriaButtonProps` | Props for the clear button. |
| `descriptionProps` | `DOMAttributes` | Props for the searchfield's description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the searchfield's error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

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

Provides state management for a search field.

`useSearchFieldState(
(props: SearchFieldProps
)): SearchFieldState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `onSubmit` | `( (value: string )) => void` | â | Handler that is called when the SearchField is submitted. |
| `onClear` | `() => void` | â | Handler that is called when the clear button is pressed. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: string )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<T> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<T> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `placeholder` | `string` | â | Temporary text that occupies the text input when it is empty. |
| `value` | `string` | â | The current value (controlled). |
| `defaultValue` | `string` | â | The default value (uncontrolled). |
| `onChange` | `( (value: T )) => void` | â | Handler that is called when the value changes. |
| `label` | `ReactNode` | â | The content to display as the label. |