# useCheckbox

Source: https://react-spectrum.adobe.com/react-aria/useCheckbox.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Checkbox).

# useCheckbox

Provides the behavior and accessibility implementation for a checkbox component.
Checkboxes allow users to select multiple items from a list of individual items, or
to mark one individual item as selected.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useCheckbox} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/checkbox "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/checkbox "View package")

## API[#](#api)

---

`useCheckbox(
props: AriaCheckboxProps,
state: ToggleState,
inputRef: RefObject<HTMLInputElement
|Â  |Â null>
): CheckboxAria`

## Features[#](#features)

---

Checkboxes can be built with the [<input>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input)
HTML element, but this can be difficult to style. `useCheckbox` helps achieve accessible checkboxes
that can be styled as needed.

- Built with a native HTML `<input>` element, which can be optionally visually
  hidden to allow custom styling
- Full support for browser features like form autofill
- Keyboard focus management and cross browser normalization
- Labeling support for assistive technology
- Indeterminate state support

## Anatomy[#](#anatomy)

---

A checkbox consists of a visual selection indicator and a label. Checkboxes support three
selection states: checked, unchecked, and indeterminate. Users may click or touch a checkbox
to toggle the selection state, or use the `Tab` key to navigate to it and the `Space` key to toggle it.

`useCheckbox` returns props to be spread onto its input element:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label wrapper element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `isSelected` | `boolean` | Whether the checkbox is selected. |
| `isPressed` | `boolean` | Whether the checkbox is in a pressed state. |
| `isDisabled` | `boolean` | Whether the checkbox is disabled. |
| `isReadOnly` | `boolean` | Whether the checkbox is read only. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

Selection state is managed by the `useToggleState`
hook in `@react-stately/toggle`. The state object should be passed as an option to `useCheckbox`.

In most cases, checkboxes should have a visual label. If the checkbox does not have a visible label,
an `aria-label` or `aria-labelledby` prop must be passed instead to identify the element to assistive
technology.

## Example[#](#example)

---

```
import {useToggleState} from 'react-stately';
import {useCheckbox} from 'react-aria';

function Checkbox(props) {
  let { children } = props;
  let state = useToggleState(props);
  let ref = React.useRef(null);
  let { inputProps, labelProps } = useCheckbox(props, state, ref);

  return (
    <label {...labelProps} style={{ display: 'block' }}>
      <input {...inputProps} ref={ref} />
      {children}
    </label>
  );
}

<Checkbox>Unsubscribe</Checkbox>
```

```
import {useToggleState} from 'react-stately';
import {useCheckbox} from 'react-aria';

function Checkbox(props) {
  let { children } = props;
  let state = useToggleState(props);
  let ref = React.useRef(null);
  let { inputProps, labelProps } = useCheckbox(
    props,
    state,
    ref
  );

  return (
    <label {...labelProps} style={{ display: 'block' }}>
      <input {...inputProps} ref={ref} />
      {children}
    </label>
  );
}

<Checkbox>Unsubscribe</Checkbox>
```

```
import {useToggleState} from 'react-stately';
import {useCheckbox} from 'react-aria';

function Checkbox(
  props
) {
  let { children } =
    props;
  let state =
    useToggleState(
      props
    );
  let ref = React.useRef(
    null
  );
  let {
    inputProps,
    labelProps
  } = useCheckbox(
    props,
    state,
    ref
  );

  return (
    <label
      {...labelProps}
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

<Checkbox>
  Unsubscribe
</Checkbox>
```

## Styling[#](#styling)

---

To build a custom styled checkbox, you can make the native input element visually hidden.
This is possible using the <`VisuallyHidden`>
utility component from `@react-aria/visually-hidden`. It is still in the DOM and accessible to
assistive technology, but invisible. This example uses SVG to build the visual checkbox,
which is hidden from screen readers with `aria-hidden`.

For keyboard accessibility, a focus ring is important to indicate which element has keyboard focus.
This is implemented with the `useFocusRing`
hook from `@react-aria/focus`. When `isFocusVisible` is true, an extra SVG element is
rendered to indicate focus. The focus ring is only visible when the user is interacting
with a keyboard, not with a mouse or touch.

```
import {mergeProps, useFocusRing, VisuallyHidden} from 'react-aria';

function Checkbox(props) {
  let state = useToggleState(props);
  let ref = React.useRef(null);
  let { inputProps, labelProps } = useCheckbox(props, state, ref);
  let { isFocusVisible, focusProps } = useFocusRing();
  let isSelected = state.isSelected && !props.isIndeterminate;

  return (
    <label
      {...labelProps}
      style={{
        display: 'flex',
        alignItems: 'center',
        opacity: props.isDisabled ? 0.4 : 1
      }}
    >
      <VisuallyHidden>
        <input {...mergeProps(inputProps, focusProps)} ref={ref} />
      </VisuallyHidden>
      <svg
        width={24}
        height={24}
        aria-hidden="true"
        style={{ marginRight: 4 }}
      >
        <rect
          x={isSelected ? 4 : 5}
          y={isSelected ? 4 : 5}
          width={isSelected ? 16 : 14}
          height={isSelected ? 16 : 14}
          fill={isSelected ? 'orange' : 'none'}
          stroke={isSelected ? 'none' : 'gray'}
          strokeWidth={2}
        />
        {isSelected &&
          (
            <path
              transform="translate(7 7)"
              d={`M3.788 9A.999.999 0 0 1 3 8.615l-2.288-3a1 1 0 1 1
            1.576-1.23l1.5 1.991 3.924-4.991a1 1 0 1 1 1.576 1.23l-4.712
            6A.999.999 0 0 1 3.788 9z`}
            />
          )}
        {props.isIndeterminate &&
          <rect x={7} y={11} width={10} height={2} fill="gray" />}
        {isFocusVisible &&
          (
            <rect
              x={1}
              y={1}
              width={22}
              height={22}
              fill="none"
              stroke="orange"
              strokeWidth={2}
            />
          )}
      </svg>
      {props.children}
    </label>
  );
}

<Checkbox>Unsubscribe</Checkbox>
```

```
import {
  mergeProps,
  useFocusRing,
  VisuallyHidden
} from 'react-aria';

function Checkbox(props) {
  let state = useToggleState(props);
  let ref = React.useRef(null);
  let { inputProps, labelProps } = useCheckbox(
    props,
    state,
    ref
  );
  let { isFocusVisible, focusProps } = useFocusRing();
  let isSelected = state.isSelected &&
    !props.isIndeterminate;

  return (
    <label
      {...labelProps}
      style={{
        display: 'flex',
        alignItems: 'center',
        opacity: props.isDisabled ? 0.4 : 1
      }}
    >
      <VisuallyHidden>
        <input
          {...mergeProps(inputProps, focusProps)}
          ref={ref}
        />
      </VisuallyHidden>
      <svg
        width={24}
        height={24}
        aria-hidden="true"
        style={{ marginRight: 4 }}
      >
        <rect
          x={isSelected ? 4 : 5}
          y={isSelected ? 4 : 5}
          width={isSelected ? 16 : 14}
          height={isSelected ? 16 : 14}
          fill={isSelected ? 'orange' : 'none'}
          stroke={isSelected ? 'none' : 'gray'}
          strokeWidth={2}
        />
        {isSelected &&
          (
            <path
              transform="translate(7 7)"
              d={`M3.788 9A.999.999 0 0 1 3 8.615l-2.288-3a1 1 0 1 1
            1.576-1.23l1.5 1.991 3.924-4.991a1 1 0 1 1 1.576 1.23l-4.712
            6A.999.999 0 0 1 3.788 9z`}
            />
          )}
        {props.isIndeterminate &&
          (
            <rect
              x={7}
              y={11}
              width={10}
              height={2}
              fill="gray"
            />
          )}
        {isFocusVisible &&
          (
            <rect
              x={1}
              y={1}
              width={22}
              height={22}
              fill="none"
              stroke="orange"
              strokeWidth={2}
            />
          )}
      </svg>
      {props.children}
    </label>
  );
}

<Checkbox>Unsubscribe</Checkbox>
```

```
import {
  mergeProps,
  useFocusRing,
  VisuallyHidden
} from 'react-aria';

function Checkbox(
  props
) {
  let state =
    useToggleState(
      props
    );
  let ref = React.useRef(
    null
  );
  let {
    inputProps,
    labelProps
  } = useCheckbox(
    props,
    state,
    ref
  );
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();
  let isSelected =
    state.isSelected &&
    !props
      .isIndeterminate;

  return (
    <label
      {...labelProps}
      style={{
        display: 'flex',
        alignItems:
          'center',
        opacity:
          props
              .isDisabled
            ? 0.4
            : 1
      }}
    >
      <VisuallyHidden>
        <input
          {...mergeProps(
            inputProps,
            focusProps
          )}
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
        <rect
          x={isSelected
            ? 4
            : 5}
          y={isSelected
            ? 4
            : 5}
          width={isSelected
            ? 16
            : 14}
          height={isSelected
            ? 16
            : 14}
          fill={isSelected
            ? 'orange'
            : 'none'}
          stroke={isSelected
            ? 'none'
            : 'gray'}
          strokeWidth={2}
        />
        {isSelected &&
          (
            <path
              transform="translate(7 7)"
              d={`M3.788 9A.999.999 0 0 1 3 8.615l-2.288-3a1 1 0 1 1
            1.576-1.23l1.5 1.991 3.924-4.991a1 1 0 1 1 1.576 1.23l-4.712
            6A.999.999 0 0 1 3.788 9z`}
            />
          )}
        {props
          .isIndeterminate &&
          (
            <rect
              x={7}
              y={11}
              width={10}
              height={2}
              fill="gray"
            />
          )}
        {isFocusVisible &&
          (
            <rect
              x={1}
              y={1}
              width={22}
              height={22}
              fill="none"
              stroke="orange"
              strokeWidth={2}
            />
          )}
      </svg>
      {props.children}
    </label>
  );
}

<Checkbox>
  Unsubscribe
</Checkbox>
```

## Styled examples[#](#styled-examples)

---

[![](/tailwind-example.3ad575ae.png)

Tailwind CSS

An animated Checkbox built with Tailwind and React Aria.](https://codesandbox.io/s/bold-river-0v44z6?file=/src/Checkbox.tsx)

## Usage[#](#usage)

---

The following examples show how to use the `Checkbox` component created in the above example.

### Default value[#](#default-value)

Checkboxes are not selected by default. The `defaultSelected` prop can be used to set the default state.

```
<Checkbox defaultSelected>Subscribe</Checkbox>
```

```
<Checkbox defaultSelected>Subscribe</Checkbox>
```

```
<Checkbox
  defaultSelected
>
  Subscribe
</Checkbox>
```

### Controlled value[#](#controlled-value)

The `isSelected` prop can be used to make the selected state controlled. The `onChange` event is fired when the user presses the checkbox, and receives the new value.

```
function Example() {
  let [selected, setSelection] = React.useState(false);

  return (
    <>
      <Checkbox isSelected={selected} onChange={setSelection}>
        Subscribe
      </Checkbox>
      <p>{`You are ${selected ? 'subscribed' : 'unsubscribed'}`}</p>
    </>
  );
 }
```

```
function Example() {
  let [selected, setSelection] = React.useState(false);

  return (
    <>
      <Checkbox
        isSelected={selected}
        onChange={setSelection}
      >
        Subscribe
      </Checkbox>
      <p>
        {`You are ${
          selected ? 'subscribed' : 'unsubscribed'
        }`}
      </p>
    </>
  );
}
```

```
function Example() {
  let [
    selected,
    setSelection
  ] = React.useState(
    false
  );

  return (
    <>
      <Checkbox
        isSelected={selected}
        onChange={setSelection}
      >
        Subscribe
      </Checkbox>
      <p>
        {`You are ${
          selected
            ? 'subscribed'
            : 'unsubscribed'
        }`}
      </p>
    </>
  );
}
```

### Indeterminate[#](#indeterminate)

A Checkbox can be in an indeterminate state, controlled using the `isIndeterminate` prop.
This overrides the appearance of the Checkbox, whether selection is controlled or uncontrolled.
The Checkbox will visually remain indeterminate until the `isIndeterminate` prop is set to false, regardless of user interaction.

```
<Checkbox isIndeterminate>Subscribe</Checkbox>
```

```
<Checkbox isIndeterminate>Subscribe</Checkbox>
```

```
<Checkbox
  isIndeterminate
>
  Subscribe
</Checkbox>
```

### Disabled[#](#disabled)

Checkboxes can be disabled using the `isDisabled` prop.

```
<Checkbox isDisabled>Subscribe</Checkbox>
```

```
<Checkbox isDisabled>Subscribe</Checkbox>
```

```
<Checkbox isDisabled>
  Subscribe
</Checkbox>
```

### Read only[#](#read-only)

The `isReadOnly` prop makes the selection immutable. Unlike `isDisabled`, the Checkbox remains focusable.
See the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/readonly) for more information.

```
<Checkbox isSelected isReadOnly>Agree</Checkbox>
```

```
<Checkbox isSelected isReadOnly>Agree</Checkbox>
```

```
<Checkbox
  isSelected
  isReadOnly
>
  Agree
</Checkbox>
```

### HTML forms[#](#html-forms)

Checkbox supports the `name` and `value` props for integration with HTML forms.

```
<Checkbox name="newsletter" value="subscribe">Subscribe</Checkbox>
```

```
<Checkbox name="newsletter" value="subscribe">
  Subscribe
</Checkbox>
```

```
<Checkbox
  name="newsletter"
  value="subscribe"
>
  Subscribe
</Checkbox>
```

## Internationalization[#](#internationalization)

---

### RTL[#](#rtl)

In right-to-left languages, the checkbox should be mirrored. The checkbox should be placed on the right
side of the label. Ensure that your CSS accounts for this.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isIndeterminate` | `boolean` | â | Indeterminism is presentational only. The indeterminate visual representation remains regardless of user interaction. |
| `children` | `ReactNode` | â | The label for the element. |
| `value` | `string` | â | The value of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefvalue). |
| `defaultSelected` | `boolean` | â | Whether the element should be selected (uncontrolled). |
| `isSelected` | `boolean` | â | Whether the element should be selected (controlled). |
| `onChange` | `( (isSelected: boolean )) => void` | â | Handler that is called when the element's selection state changes. |
| `isDisabled` | `boolean` | â | Whether the input is disabled. |
| `isReadOnly` | `boolean` | â | Whether the input can be selected but not changed by the user. |
| `isRequired` | `boolean` | â | Whether user input is required on the input before form submission. |
| `isInvalid` | `boolean` | â | Whether the input value is invalid. |
| `validationBehavior` | `'aria' |Â 'native'` | `'aria'` | Whether to use native HTML form validation to prevent form submission when the value is missing or invalid, or mark the field as required or invalid via ARIA. |
| `validate` | `( (value: boolean )) => ValidationError |Â true |Â null |Â undefined` | â | A function that returns an error message if a given value is invalid. Validation errors are displayed to the user when the form is submitted if `validationBehavior="native"`. For realtime validation, use the `isInvalid` prop instead. |
| `autoFocus` | `boolean` | â | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | â | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | â | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | â | Handler that is called when a key is released. |
| `name` | `string` | â | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | â | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `aria-errormessage` | `string` | â | Identifies the element that provides an error message for the object. |
| `onPress` | `( (e: PressEvent )) => void` | â | Handler that is called when the press is released over the target. |
| `onPressStart` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction starts. |
| `onPressEnd` | `( (e: PressEvent )) => void` | â | Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. |
| `onPressChange` | `( (isPressed: boolean )) => void` | â | Handler that is called when the press state changes. |
| `onPressUp` | `( (e: PressEvent )) => void` | â | Handler that is called when a press is released over the target, regardless of whether it started on the target or not. |
| `onClick` | `( (e: MouseEvent<FocusableElement> )) => void` | â | **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. |

`'valid' |Â 'invalid'`

`string |Â string[]`

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

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`

### Properties

| Name | Type | Description |
| --- | --- | --- |
| `isSelected` | `boolean` | Whether the toggle is selected. |
| `defaultSelected` | `boolean` | Whether the toggle is selected by default. |

### Methods

| Method | Description |
| --- | --- |
| `setSelected( (isSelected: boolean )): void` | Updates selection state. |
| `toggle(): void` | Toggle the selection state. |

| Name | Type | Description |
| --- | --- | --- |
| `current` | `T` |  |

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label wrapper element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `isSelected` | `boolean` | Whether the checkbox is selected. |
| `isPressed` | `boolean` | Whether the checkbox is in a pressed state. |
| `isDisabled` | `boolean` | Whether the checkbox is disabled. |
| `isReadOnly` | `boolean` | Whether the checkbox is read only. |
| `isInvalid` | `boolean` | Whether the input value is invalid. |
| `validationErrors` | `string[]` | The current error messages for the input if it is invalid, otherwise an empty array. |
| `validationDetails` | `ValidityState` | The native validation details for the input. |

Provides state management for toggle components like checkboxes and switches.

`useToggleState(
(props: ToggleStateOptions
)): ToggleState`

| Name | Type | Description |
| --- | --- | --- |
| `defaultSelected` | `boolean` | Whether the element should be selected (uncontrolled). |
| `isSelected` | `boolean` | Whether the element should be selected (controlled). |
| `onChange` | `( (isSelected: boolean )) => void` | Handler that is called when the element's selection state changes. |
| `isDisabled` | `boolean` | Whether the input is disabled. |
| `isReadOnly` | `boolean` | Whether the input can be selected but not changed by the user. |

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

All DOM attributes supported across both HTML and SVG elements.

**Extends**: `AriaAttributes, ReactDOMAttributes`

| Name | Type | Description |
| --- | --- | --- |
| `id` | `string |Â undefined` |  |
| `role` | `AriaRole |Â undefined` |  |
| `tabIndex` | `number |Â undefined` |  |
| `style` | `CSSProperties |Â undefined` |  |
| `className` | `string |Â undefined` |  |