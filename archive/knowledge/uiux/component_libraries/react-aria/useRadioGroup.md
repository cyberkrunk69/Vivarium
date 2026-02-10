# useRadioGroup

Source: https://react-spectrum.adobe.com/react-aria/useRadioGroup.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../RadioGroup).

# useRadioGroup

Provides the behavior and accessibility implementation for a radio group component.
Radio groups allow users to select a single item from a list of mutually exclusive options.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useRadioGroup, useRadio} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/radiobutton/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/radio "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/radio "View package")

## API[#](#api)

---

`useRadioGroup(
(props: AriaRadioGroupProps,
, state: RadioGroupState
)): RadioGroupAria`
`useRadio(
props: AriaRadioProps,
state: RadioGroupState,
ref: RefObject<HTMLInputElement
|Â  |Â null>
): RadioAria`

## Features[#](#features)

---

Radio groups can be built in HTML with the
[<fieldset>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/fieldset)
and [<input>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) elements,
however these can be difficult to style. `useRadioGroup` and `useRadio` help achieve accessible
radio groups that can be styled as needed.

- Radio groups are exposed to assistive technology via ARIA
- Each radio is built with a native HTML `<input>` element, which can be optionally visually
  hidden to allow custom styling
- Full support for browser features like form autofill and validation
- Keyboard focus management and cross browser normalization
- Group and radio labeling support for assistive technology

## Anatomy[#](#anatomy)

---

A radio group consists of a set of radio buttons, and a label. Each radio
includes a label and a visual selection indicator. A single radio button
within the group can be selected at a time. Users may click or touch a radio
button to select it, or use the `Tab` key to navigate to the group, the arrow keys
to navigate within the group, and the `Space` key to select an option.

`useRadioGroup` returns props for the group and its label, which you should spread
onto the appropriate element:

| Name | Type | Description |
| --- | --- | --- |
| `radioGroupProps` | `DOMAttributes` | Props for the radio group wrapper element. |
| `labelProps` | `DOMAttributes` | Props for the radio group's visible label (if any). |
| `descriptionProps` | `DOMAttributes` | Props for the radio group description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the radio group error message element, if any. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

`useRadio` returns props for an individual radio, along with states that can be used for styling:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label wrapper element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `isDisabled` | `boolean` | Whether the radio is disabled. |
| `isSelected` | `boolean` | Whether the radio is currently selected. |
| `isPressed` | `boolean` | Whether the radio is in a pressed state. |

Selection state is managed by the `useRadioGroupState`
hook in `@react-stately/radio`. The state object should be passed as an option to `useRadio`.

Individual radio buttons must have a visual label. If the radio group does not have a visible label,
an `aria-label` or `aria-labelledby` prop must be passed instead to identify the element to assistive
technology.

## Example[#](#example)

---

This example uses native input elements for the radios, and React context to share state from the group
to each radio. An HTML `<label>` element wraps the native input and the text to provide an implicit label
for the radio.

```
import {useRadioGroupState} from 'react-stately';
import {useRadio, useRadioGroup} from 'react-aria';

let RadioContext = React.createContext(null);

function RadioGroup(props) {
  let { children, label, description, errorMessage } = props;
  let state = useRadioGroupState(props);
  let { radioGroupProps, labelProps, descriptionProps, errorMessageProps } =
    useRadioGroup(props, state);

  return (
    <div {...radioGroupProps}>
      <span {...labelProps}>{label}</span>
      <RadioContext.Provider value={state}>
        {children}
      </RadioContext.Provider>
      {description && (
        <div {...descriptionProps} style={{ fontSize: 12 }}>{description}</div>
      )}
      {errorMessage && state.isInvalid &&
        (
          <div {...errorMessageProps} style={{ color: 'red', fontSize: 12 }}>
            {errorMessage}
          </div>
        )}
    </div>
  );
}

function Radio(props) {
  let { children } = props;
  let state = React.useContext(RadioContext);
  let ref = React.useRef(null);
  let { inputProps } = useRadio(props, state, ref);

  return (
    <label style={{ display: 'block' }}>
      <input {...inputProps} ref={ref} />
      {children}
    </label>
  );
}

<RadioGroup label="Favorite pet">
  <Radio value="dogs">Dogs</Radio>
  <Radio value="cats">Cats</Radio>
</RadioGroup>
```

```
import {useRadioGroupState} from 'react-stately';
import {useRadio, useRadioGroup} from 'react-aria';

let RadioContext = React.createContext(null);

function RadioGroup(props) {
  let { children, label, description, errorMessage } =
    props;
  let state = useRadioGroupState(props);
  let {
    radioGroupProps,
    labelProps,
    descriptionProps,
    errorMessageProps
  } = useRadioGroup(props, state);

  return (
    <div {...radioGroupProps}>
      <span {...labelProps}>{label}</span>
      <RadioContext.Provider value={state}>
        {children}
      </RadioContext.Provider>
      {description && (
        <div {...descriptionProps} style={{ fontSize: 12 }}>
          {description}
        </div>
      )}
      {errorMessage && state.isInvalid &&
        (
          <div
            {...errorMessageProps}
            style={{ color: 'red', fontSize: 12 }}
          >
            {errorMessage}
          </div>
        )}
    </div>
  );
}

function Radio(props) {
  let { children } = props;
  let state = React.useContext(RadioContext);
  let ref = React.useRef(null);
  let { inputProps } = useRadio(props, state, ref);

  return (
    <label style={{ display: 'block' }}>
      <input {...inputProps} ref={ref} />
      {children}
    </label>
  );
}

<RadioGroup label="Favorite pet">
  <Radio value="dogs">Dogs</Radio>
  <Radio value="cats">Cats</Radio>
</RadioGroup>
```

```
import {useRadioGroupState} from 'react-stately';
import {
  useRadio,
  useRadioGroup
} from 'react-aria';

let RadioContext = React
  .createContext(null);

function RadioGroup(
  props
) {
  let {
    children,
    label,
    description,
    errorMessage
  } = props;
  let state =
    useRadioGroupState(
      props
    );
  let {
    radioGroupProps,
    labelProps,
    descriptionProps,
    errorMessageProps
  } = useRadioGroup(
    props,
    state
  );

  return (
    <div
      {...radioGroupProps}
    >
      <span
        {...labelProps}
      >
        {label}
      </span>
      <RadioContext.Provider
        value={state}
      >
        {children}
      </RadioContext.Provider>
      {description && (
        <div
          {...descriptionProps}
          style={{
            fontSize: 12
          }}
        >
          {description}
        </div>
      )}
      {errorMessage &&
        state
          .isInvalid &&
        (
          <div
            {...errorMessageProps}
            style={{
              color:
                'red',
              fontSize:
                12
            }}
          >
            {errorMessage}
          </div>
        )}
    </div>
  );
}

function Radio(props) {
  let { children } =
    props;
  let state = React
    .useContext(
      RadioContext
    );
  let ref = React.useRef(
    null
  );
  let { inputProps } =
    useRadio(
      props,
      state,
      ref
    );

  return (
    <label
      style={{
        display: 'block'
      }}
    >
      <input
        {...inputProps}
        ref={ref}
      />
      {children}
    </label>
  );
}

<RadioGroup label="Favorite pet">
  <Radio value="dogs">
    Dogs
  </Radio>
  <Radio value="cats">
    Cats
  </Radio>
</RadioGroup>
```

## Styling[#](#styling)

---

To build a custom styled radio button, you can make the native input element visually hidden.
This is possible using the <`VisuallyHidden`>
utility component from `@react-aria/visually-hidden`. It is still in the DOM and accessible to
assistive technology, but invisible. This example uses SVG to build the visual radio button,
which is hidden from screen readers with `aria-hidden`.

For keyboard accessibility, a focus ring is important to indicate which element has keyboard focus.
This is implemented with the `useFocusRing`
hook from `@react-aria/focus`. When `isFocusVisible` is true, an extra SVG element is rendered to
indicate focus. The focus ring is only visible when the user is interacting with a keyboard,
not with a mouse or touch.

```
import {useFocusRing, VisuallyHidden} from 'react-aria';

// RadioGroup is the same as in the previous example
let RadioContext = React.createContext(null);

function RadioGroup(props) {
  let { children, label, description } = props;
  let state = useRadioGroupState(props);
  let {
    radioGroupProps,
    labelProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useRadioGroup(props, state);

  return (
    <div {...radioGroupProps}>
      <span {...labelProps}>{label}</span>
      <RadioContext.Provider value={state}>
        {children}
      </RadioContext.Provider>
      {description && (
        <div {...descriptionProps} style={{ fontSize: 12 }}>{description}</div>
      )}
      {isInvalid &&
        (
          <div {...errorMessageProps} style={{ color: 'red', fontSize: 12 }}>
            {validationErrors.join(' ')}
          </div>
        )}
    </div>
  );
}

function Radio(props) {
  let { children } = props;
  let state = React.useContext(RadioContext);
  let ref = React.useRef(null);
  let { inputProps, isSelected, isDisabled } = useRadio(props, state, ref);
  let { isFocusVisible, focusProps } = useFocusRing();
  let strokeWidth = isSelected ? 6 : 2;

  return (
    <label
      style={{
        display: 'flex',
        alignItems: 'center',
        opacity: isDisabled ? 0.4 : 1
      }}
    >
      <VisuallyHidden>
        <input {...inputProps} {...focusProps} ref={ref} />
      </VisuallyHidden>
      <svg
        width={24}
        height={24}
        aria-hidden="true"
        style={{ marginRight: 4 }}
      >
        <circle
          cx={12}
          cy={12}
          r={8 - strokeWidth / 2}
          fill="none"
          stroke={isSelected ? 'orange' : 'gray'}
          strokeWidth={strokeWidth}
        />
        {isFocusVisible &&
          (
            <circle
              cx={12}
              cy={12}
              r={11}
              fill="none"
              stroke="orange"
              strokeWidth={2}
            />
          )}
      </svg>
      {children}
    </label>
  );
}

<RadioGroup label="Favorite pet">
  <Radio value="dogs">Dogs</Radio>
  <Radio value="cats">Cats</Radio>
</RadioGroup>
```

```
import {useFocusRing, VisuallyHidden} from 'react-aria';

// RadioGroup is the same as in the previous example
let RadioContext = React.createContext(null);

function RadioGroup(props) {
  let { children, label, description } = props;
  let state = useRadioGroupState(props);
  let {
    radioGroupProps,
    labelProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useRadioGroup(props, state);

  return (
    <div {...radioGroupProps}>
      <span {...labelProps}>{label}</span>
      <RadioContext.Provider value={state}>
        {children}
      </RadioContext.Provider>
      {description && (
        <div {...descriptionProps} style={{ fontSize: 12 }}>
          {description}
        </div>
      )}
      {isInvalid &&
        (
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

function Radio(props) {
  let { children } = props;
  let state = React.useContext(RadioContext);
  let ref = React.useRef(null);
  let { inputProps, isSelected, isDisabled } = useRadio(
    props,
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();
  let strokeWidth = isSelected ? 6 : 2;

  return (
    <label
      style={{
        display: 'flex',
        alignItems: 'center',
        opacity: isDisabled ? 0.4 : 1
      }}
    >
      <VisuallyHidden>
        <input {...inputProps} {...focusProps} ref={ref} />
      </VisuallyHidden>
      <svg
        width={24}
        height={24}
        aria-hidden="true"
        style={{ marginRight: 4 }}
      >
        <circle
          cx={12}
          cy={12}
          r={8 - strokeWidth / 2}
          fill="none"
          stroke={isSelected ? 'orange' : 'gray'}
          strokeWidth={strokeWidth}
        />
        {isFocusVisible &&
          (
            <circle
              cx={12}
              cy={12}
              r={11}
              fill="none"
              stroke="orange"
              strokeWidth={2}
            />
          )}
      </svg>
      {children}
    </label>
  );
}

<RadioGroup label="Favorite pet">
  <Radio value="dogs">Dogs</Radio>
  <Radio value="cats">Cats</Radio>
</RadioGroup>
```

```
import {
  useFocusRing,
  VisuallyHidden
} from 'react-aria';

// RadioGroup is the same as in the previous example
let RadioContext = React
  .createContext(null);

function RadioGroup(
  props
) {
  let {
    children,
    label,
    description
  } = props;
  let state =
    useRadioGroupState(
      props
    );
  let {
    radioGroupProps,
    labelProps,
    descriptionProps,
    errorMessageProps,
    isInvalid,
    validationErrors
  } = useRadioGroup(
    props,
    state
  );

  return (
    <div
      {...radioGroupProps}
    >
      <span
        {...labelProps}
      >
        {label}
      </span>
      <RadioContext.Provider
        value={state}
      >
        {children}
      </RadioContext.Provider>
      {description && (
        <div
          {...descriptionProps}
          style={{
            fontSize: 12
          }}
        >
          {description}
        </div>
      )}
      {isInvalid &&
        (
          <div
            {...errorMessageProps}
            style={{
              color:
                'red',
              fontSize:
                12
            }}
          >
            {validationErrors
              .join(' ')}
          </div>
        )}
    </div>
  );
}

function Radio(props) {
  let { children } =
    props;
  let state = React
    .useContext(
      RadioContext
    );
  let ref = React.useRef(
    null
  );
  let {
    inputProps,
    isSelected,
    isDisabled
  } = useRadio(
    props,
    state,
    ref
  );
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();
  let strokeWidth =
    isSelected ? 6 : 2;

  return (
    <label
      style={{
        display: 'flex',
        alignItems:
          'center',
        opacity:
          isDisabled
            ? 0.4
            : 1
      }}
    >
      <VisuallyHidden>
        <input
          {...inputProps}
          {...focusProps}
          ref={ref}
        />
      </VisuallyHidden>
      <svg
        width={24}
        height={24}
        aria-hidden="true"
        style={{
          marginRight: 4
        }}
      >
        <circle
          cx={12}
          cy={12}
          r={8 -
            strokeWidth /
              2}
          fill="none"
          stroke={isSelected
            ? 'orange'
            : 'gray'}
          strokeWidth={strokeWidth}
        />
        {isFocusVisible &&
          (
            <circle
              cx={12}
              cy={12}
              r={11}
              fill="none"
              stroke="orange"
              strokeWidth={2}
            />
          )}
      </svg>
      {children}
    </label>
  );
}

<RadioGroup label="Favorite pet">
  <Radio value="dogs">
    Dogs
  </Radio>
  <Radio value="cats">
    Cats
  </Radio>
</RadioGroup>
```

## Styled examples[#](#styled-examples)

---

[![](/swatch-example.41f639bc.png)

Swatch Group

A color swatch picker built with Tailwind CSS.](https://codesandbox.io/s/bold-wood-pxm478?file=/src/SwatchGroup.tsx)
[![](/card-example.0dbe729a.png)

Selectable Cards

A selectable card group built with Styled Components.](https://codesandbox.io/s/recursing-night-pu6w2g?file=/src/CardGroup.tsx)
[![](/buttongroup-example.165f9e91.png)

Button Group

A single-selectable segmented button group.](https://codesandbox.io/s/epic-faraday-qoiy0l?file=/src/ButtonGroup.js)

## Usage[#](#usage)

---

The following examples show how to use the `RadioGroup` component created in the above example.

### Default value[#](#default-value)

An initial, uncontrolled value can be provided to the RadioGroup using the `defaultValue` prop, which accepts a value corresponding with the `value` prop of each Radio.

```
<RadioGroup label="Are you a wizard?" defaultValue="yes">
  <Radio value="yes">Yes</Radio>
  <Radio value="no">No</Radio>
</RadioGroup>
```

```
<RadioGroup label="Are you a wizard?" defaultValue="yes">
  <Radio value="yes">Yes</Radio>
  <Radio value="no">No</Radio>
</RadioGroup>
```

```
<RadioGroup
  label="Are you a wizard?"
  defaultValue="yes"
>
  <Radio value="yes">
    Yes
  </Radio>
  <Radio value="no">
    No
  </Radio>
</RadioGroup>
```

### Controlled value[#](#controlled-value)

A controlled value can be provided using the `value` prop, which accepts a value corresponding with the `value` prop of each Radio.
The `onChange` event is fired when the user selects a radio.

```
function Example() {
  let [selected, setSelected] = React.useState(null);

  return (
    <>
      <RadioGroup
        label="Favorite avatar"
        value={selected}
        onChange={setSelected}
      >
        <Radio value="wizard">Wizard</Radio>
        <Radio value="dragon">Dragon</Radio>
      </RadioGroup>
      <p>You have selected: {selected}</p>
    </>
  );
}
```

```
function Example() {
  let [selected, setSelected] = React.useState(null);

  return (
    <>
      <RadioGroup
        label="Favorite avatar"
        value={selected}
        onChange={setSelected}
      >
        <Radio value="wizard">Wizard</Radio>
        <Radio value="dragon">Dragon</Radio>
      </RadioGroup>
      <p>You have selected: {selected}</p>
    </>
  );
}
```

```
function Example() {
  let [
    selected,
    setSelected
  ] = React.useState(
    null
  );

  return (
    <>
      <RadioGroup
        label="Favorite avatar"
        value={selected}
        onChange={setSelected}
      >
        <Radio value="wizard">
          Wizard
        </Radio>
        <Radio value="dragon">
          Dragon
        </Radio>
      </RadioGroup>
      <p>
        You have
        selected:{' '}
        {selected}
      </p>
    </>
  );
}
```

### Description[#](#description)

The `description` prop can be used to associate additional help text with a radio group.

```
<RadioGroup label="Favorite pet" description="Select your favorite pet.">
  <Radio value="dogs">Dogs</Radio>
  <Radio value="cats">Cats</Radio>
</RadioGroup>
```

```
<RadioGroup
  label="Favorite pet"
  description="Select your favorite pet."
>
  <Radio value="dogs">Dogs</Radio>
  <Radio value="cats">Cats</Radio>
</RadioGroup>
```

```
<RadioGroup
  label="Favorite pet"
  description="Select your favorite pet."
>
  <Radio value="dogs">
    Dogs
  </Radio>
  <Radio value="cats">
    Cats
  </Radio>
</RadioGroup>
```

### Validation[#](#validation)

RadioGroup supports the `isRequired` prop to ensure the user selects an option, as well as custom client and server-side validation. It can also be integrated with other form libraries. See the [Forms](../forms) guide to learn more.

When a RadioGroup has the `validationBehavior="native"` prop, validation errors block form submission. To display validation errors, use the `validationErrors` and `errorMessageProps` returned by `useRadioGroup`. This allows you to render error messages from all of the above sources with consistent custom styles.

```
<form>
  <RadioGroup
    label="Favorite pet"
    name="pet"
    isRequired
    validationBehavior="native"
  >    <Radio value="dogs">Dog</Radio>
    <Radio value="cats">Cat</Radio>
    <Radio value="dragon">Dragon</Radio>
  </RadioGroup>
  <input type="submit" style={{ marginTop: 8 }} />
</form>
```

```
<form>
  <RadioGroup
    label="Favorite pet"
    name="pet"
    isRequired
    validationBehavior="native"
  >    <Radio value="dogs">Dog</Radio>
    <Radio value="cats">Cat</Radio>
    <Radio value="dragon">Dragon</Radio>
  </RadioGroup>
  <input type="submit" style={{ marginTop: 8 }} />
</form>
```

```
<form>
  <RadioGroup
    label="Favorite pet"
    name="pet"
    isRequired
    validationBehavior="native"
  >    <Radio value="dogs">
      Dog
    </Radio>
    <Radio value="cats">
      Cat
    </Radio>
    <Radio value="dragon">
      Dragon
    </Radio>
  </RadioGroup>
  <input
    type="submit"
    style={{
      marginTop: 8
    }}
  />
</form>
```

### Disabled[#](#disabled)

The entire RadioGroup can be disabled with the `isDisabled` prop.

```
<RadioGroup label="Favorite sport" isDisabled>
  <Radio value="soccer">Soccer</Radio>
  <Radio value="baseball">Baseball</Radio>
  <Radio value="basketball">Basketball</Radio>
</RadioGroup>
```

```
<RadioGroup label="Favorite sport" isDisabled>
  <Radio value="soccer">Soccer</Radio>
  <Radio value="baseball">Baseball</Radio>
  <Radio value="basketball">Basketball</Radio>
</RadioGroup>
```

```
<RadioGroup
  label="Favorite sport"
  isDisabled
>
  <Radio value="soccer">
    Soccer
  </Radio>
  <Radio value="baseball">
    Baseball
  </Radio>
  <Radio value="basketball">
    Basketball
  </Radio>
</RadioGroup>
```

To disable an individual radio, pass `isDisabled` to the `Radio` instead.

```
<RadioGroup label="Favorite sport">
  <Radio value="soccer">Soccer</Radio>
  <Radio value="baseball" isDisabled>Baseball</Radio>
  <Radio value="basketball">Basketball</Radio>
</RadioGroup>
```

```
<RadioGroup label="Favorite sport">
  <Radio value="soccer">Soccer</Radio>
  <Radio value="baseball" isDisabled>Baseball</Radio>
  <Radio value="basketball">Basketball</Radio>
</RadioGroup>
```

```
<RadioGroup label="Favorite sport">
  <Radio value="soccer">
    Soccer
  </Radio>
  <Radio
    value="baseball"
    isDisabled
  >
    Baseball
  </Radio>
  <Radio value="basketball">
    Basketball
  </Radio>
</RadioGroup>
```

### Read only[#](#read-only)

The `isReadOnly` prop makes the selection immutable. Unlike `isDisabled`, the RadioGroup remains focusable.
See the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/readonly) for more information.

```
<RadioGroup label="Favorite avatar" defaultValue="wizard" isReadOnly>
  <Radio value="wizard">Wizard</Radio>
  <Radio value="dragon">Dragon</Radio>
</RadioGroup>
```

```
<RadioGroup
  label="Favorite avatar"
  defaultValue="wizard"
  isReadOnly
>
  <Radio value="wizard">Wizard</Radio>
  <Radio value="dragon">Dragon</Radio>
</RadioGroup>
```

```
<RadioGroup
  label="Favorite avatar"
  defaultValue="wizard"
  isReadOnly
>
  <Radio value="wizard">
    Wizard
  </Radio>
  <Radio value="dragon">
    Dragon
  </Radio>
</RadioGroup>
```

### HTML forms[#](#html-forms)

RadioGroup supports the `name` prop, paired with the Radio `value` prop, for integration with HTML forms.

```
<RadioGroup label="Favorite pet" name="pet">
  <Radio value="dogs">Dogs</Radio>
  <Radio value="cats">Cats</Radio>
</RadioGroup>
```

```
<RadioGroup label="Favorite pet" name="pet">
  <Radio value="dogs">Dogs</Radio>
  <Radio value="cats">Cats</Radio>
</RadioGroup>
```

```
<RadioGroup
  label="Favorite pet"
  name="pet"
>
  <Radio value="dogs">
    Dogs
  </Radio>
  <Radio value="cats">
    Cats
  </Radio>
</RadioGroup>
```

## Internationalization[#](#internationalization)

---

### RTL[#](#rtl)

In right-to-left languages, the radio group and radio buttons should be mirrored.
The group should be right-aligned, and the radio should be placed on the right
side of the label. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `orientation` | `Orientation` | `'vertical'` | The axis the Radio Button(s) should align with. |
| `value` | `string |Â null` | â | The current value (controlled). |
| `defaultValue` | `string |Â null` | â | The default value (uncontrolled). |
| `onChange` | `( (value: string )) => void` | â | Handler that is called when the value changes. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: string |Â  |Â null )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `aria-errormessage` | `string` | â | Identifies the element that provides an error message for the object. |

`'horizontal' |Â 'vertical'`

`'valid' |Â 'invalid'`

`string |Â string[]`

| Name | Type | Description |
| --- | --- | --- |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `isDisabled` | `boolean` | Whether the radio group is disabled. |
| `isReadOnly` | `boolean` | Whether the radio group is read only. |
| `isRequired` | `boolean` | Whether the radio group is required. |
| `isInvalid` | `boolean` | Whether the radio group is invalid. |
| `selectedValue` | `string |Â null` | The currently selected value. |
| `defaultSelectedValue` | `string |Â null` | The default selected value. |
| `lastFocusedValue` | `string |Â null` | The value of the last focused radio. |
| `realtimeValidation` | `ValidationResult` | Realtime validation results, updated as the user edits the value. |
| `displayValidation` | `ValidationResult` | Currently displayed validation results, updated when the user commits their changes. |

### Methods

| Method | Description |
| --- | --- |
| `setSelectedValue( (value: string |Â  |Â null )): void` | Sets the selected value. |
| `setLastFocusedValue( (value: string |Â  |Â null )): void` | Sets the last focused value. |
| `updateValidation( (result: ValidationResult )): void` | Updates the current validation result. Not displayed to the user until `commitValidation` is called. |
| `resetValidation(): void` | Resets the displayed validation state to valid when the user resets the form. |
| `commitValidation(): void` | Commits the realtime validation so it is displayed to the user. |

| Name | Type | Description |
| --- | --- | --- |
| `radioGroupProps` | `DOMAttributes` | Props for the radio group wrapper element. |
| `labelProps` | `DOMAttributes` | Props for the radio group's visible label (if any). |
| `descriptionProps` | `DOMAttributes` | Props for the radio group description element, if any. |
| `errorMessageProps` | `DOMAttributes` | Props for the radio group error message element, if any. |
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

| Name | Type | Description |
| --- | --- | --- |
| `value` | `string` | The value of the radio button, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/radio#Value). |
| `children` | `ReactNode` | The label for the Radio. Accepts any renderable node. |
| `isDisabled` | `boolean` | Whether the radio button is disabled or not. Shows that a selection exists, but is not available in that circumstance. |
| `autoFocus` | `boolean` | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | Handler that is called when a key is released. |
| `id` | `string` | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `onPress` | `( (e: PressEvent )) => void` | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

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

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label wrapper element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `isDisabled` | `boolean` | Whether the radio is disabled. |
| `isSelected` | `boolean` | Whether the radio is currently selected. |
| `isPressed` | `boolean` | Whether the radio is in a pressed state. |

Provides state management for a radio group component. Provides a name for the group,
and manages selection and focus state.

`useRadioGroupState(
(props: RadioGroupProps
)): RadioGroupState`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `orientation` | `Orientation` | `'vertical'` | The axis the Radio Button(s) should align with. |
| `value` | `string |Â null` | â | The current value (controlled). |
| `defaultValue` | `string |Â null` | â | The default value (uncontrolled). |
| `onChange` | `( (value: string )) => void` | â | Handler that is called when the value changes. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: string |Â  |Â null )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `label` | `ReactNode` | â | The content to display as the label. |
| `description` | `ReactNode` | â | A description for the field. Provides a hint such as specific requirements for what to choose. |
| `errorMessage` | `ReactNode |Â ( (v: ValidationResult )) => ReactNode` | â | An error message for the field. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |

VisuallyHidden hides its children visually, while keeping content visible
to screen readers.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `children` | `ReactNode` | â | The content to visually hide. |
| `elementType` | `string |Â JSXElementConstructor<any>` | `'div'` | The element type for the container. |
| `isFocusable` | `boolean` | â | Whether the element should become visible on focus, for example skip links. |
| `id` | `string |Â undefined` | â |  |
| `role` | `AriaRole |Â undefined` | â |  |
| `tabIndex` | `number |Â undefined` | â |  |
| `style` | `CSSProperties |Â undefined` | â |  |
| `className` | `string |Â undefined` | â |  |

Determines whether a focus ring should be shown to indicate keyboard focus.
Focus rings are visible only when the user is interacting with a keyboard,
not with a mouse, touch, or other input methods.

`useFocusRing(
(props: AriaFocusRingProps
)): FocusRingAria`

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `within` | `boolean` | `'false'` | Whether to show the focus ring when something inside the container element has focus (true), or only if the container itself has focus (false). |
| `isTextInput` | `boolean` | â | Whether the element is a text input. |
| `autoFocus` | `boolean` | â | Whether the element will be auto focused. |

| Name | Type | Description |
| --- | --- | --- |
| `isFocused` | `boolean` | Whether the element is currently focused. |
| `isFocusVisible` | `boolean` | Whether keyboard focus should be visible. |
| `focusProps` | `DOMAttributes` | Props to apply to the container element with the focus ring. |