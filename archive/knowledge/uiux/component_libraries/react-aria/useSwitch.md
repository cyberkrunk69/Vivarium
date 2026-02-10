# useSwitch

Source: https://react-spectrum.adobe.com/react-aria/useSwitch.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Switch).

# useSwitch

Provides the behavior and accessibility implementation for a switch component.
A switch is similar to a checkbox, but represents on/off values as opposed to selection.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useSwitch} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/switch/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/switch "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/switch "View package")

## API[#](#api)

---

`useSwitch(
props: AriaSwitchProps,
state: ToggleState,
ref: RefObject<HTMLInputElement
|Â  |Â null>
): SwitchAria`

## Features[#](#features)

---

There is no native HTML element with switch styling. `<input type="checkbox">`
is the closest semantically, but isn't styled or exposed to assistive technology
as a switch. `useSwitch` helps achieve accessible switches that can be styled as needed.

- Built with a native HTML `<input>` element, which can be optionally visually
  hidden to allow custom styling
- Full support for browser features like form autofill
- Keyboard focus management and cross browser normalization
- Labeling support for screen readers
- Exposed as a switch to assistive technology via ARIA

## Anatomy[#](#anatomy)

---

A switch consists of a visual selection indicator and a label. Users may click or touch a switch
to toggle the selection state, or use the `Tab` key to navigate to it and the `Space` key to toggle it.

`useSwitch` returns props to be spread onto its input element:

| Name | Type | Description |
| --- | --- | --- |
| `labelProps` | `LabelHTMLAttributes<HTMLLabelElement>` | Props for the label wrapper element. |
| `inputProps` | `InputHTMLAttributes<HTMLInputElement>` | Props for the input element. |
| `isSelected` | `boolean` | Whether the switch is selected. |
| `isPressed` | `boolean` | Whether the switch is in a pressed state. |
| `isDisabled` | `boolean` | Whether the switch is disabled. |
| `isReadOnly` | `boolean` | Whether the switch is read only. |

Selection state is managed by the `useToggleState`
hook in `@react-stately/toggle`. The state object should be passed as an option to `useSwitch`.

In most cases, switches should have a visual label. If the switch does not have a visible label,
an `aria-label` or `aria-labelledby` prop must be passed instead to identify the element to assistive
technology.

## Example[#](#example)

---

This example uses SVG to build the switch, with a visually hidden native input to represent
the switch for accessibility. This is possible using
the <`VisuallyHidden`>
utility component from `@react-aria/visually-hidden`. It is still in the DOM and accessible to assistive technology,
but invisible. The SVG element is the visual representation, and is hidden from screen readers
with `aria-hidden`.

For keyboard accessibility, a focus ring is important to indicate which element has keyboard focus.
This is implemented with the `useFocusRing`
hook from `@react-aria/focus`. When `isFocusVisible` is true, an extra SVG element is rendered to
indicate focus. The focus ring is only visible when the user is interacting with a keyboard,
not with a mouse or touch.

```
import {useToggleState} from 'react-stately';
import {useFocusRing, useSwitch, VisuallyHidden} from 'react-aria';

function Switch(props) {
  let state = useToggleState(props);
  let ref = React.useRef(null);
  let { inputProps } = useSwitch(props, state, ref);
  let { isFocusVisible, focusProps } = useFocusRing();

  return (
    <label
      style={{
        display: 'flex',
        alignItems: 'center',
        opacity: props.isDisabled ? 0.4 : 1
      }}
    >
      <VisuallyHidden>
        <input {...inputProps} {...focusProps} ref={ref} />
      </VisuallyHidden>
      <svg
        width={40}
        height={24}
        aria-hidden="true"
        style={{ marginRight: 4 }}
      >
        <rect
          x={4}
          y={4}
          width={32}
          height={16}
          rx={8}
          fill={state.isSelected ? 'orange' : 'gray'}
        />
        <circle
          cx={state.isSelected ? 28 : 12}
          cy={12}
          r={5}
          fill="white"
        />
        {isFocusVisible &&
          (
            <rect
              x={1}
              y={1}
              width={38}
              height={22}
              rx={11}
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

<Switch>Low power mode</Switch>
```

```
import {useToggleState} from 'react-stately';
import {
  useFocusRing,
  useSwitch,
  VisuallyHidden
} from 'react-aria';

function Switch(props) {
  let state = useToggleState(props);
  let ref = React.useRef(null);
  let { inputProps } = useSwitch(props, state, ref);
  let { isFocusVisible, focusProps } = useFocusRing();

  return (
    <label
      style={{
        display: 'flex',
        alignItems: 'center',
        opacity: props.isDisabled ? 0.4 : 1
      }}
    >
      <VisuallyHidden>
        <input {...inputProps} {...focusProps} ref={ref} />
      </VisuallyHidden>
      <svg
        width={40}
        height={24}
        aria-hidden="true"
        style={{ marginRight: 4 }}
      >
        <rect
          x={4}
          y={4}
          width={32}
          height={16}
          rx={8}
          fill={state.isSelected ? 'orange' : 'gray'}
        />
        <circle
          cx={state.isSelected ? 28 : 12}
          cy={12}
          r={5}
          fill="white"
        />
        {isFocusVisible &&
          (
            <rect
              x={1}
              y={1}
              width={38}
              height={22}
              rx={11}
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

<Switch>Low power mode</Switch>
```

```
import {useToggleState} from 'react-stately';
import {
  useFocusRing,
  useSwitch,
  VisuallyHidden
} from 'react-aria';

function Switch(props) {
  let state =
    useToggleState(
      props
    );
  let ref = React.useRef(
    null
  );
  let { inputProps } =
    useSwitch(
      props,
      state,
      ref
    );
  let {
    isFocusVisible,
    focusProps
  } = useFocusRing();

  return (
    <label
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
          {...inputProps}
          {...focusProps}
          ref={ref}
        />
      </VisuallyHidden>
      <svg
        width={40}
        height={24}
        aria-hidden="true"
        style={{
          marginRight: 4
        }}
      >
        <rect
          x={4}
          y={4}
          width={32}
          height={16}
          rx={8}
          fill={state
              .isSelected
            ? 'orange'
            : 'gray'}
        />
        <circle
          cx={state
              .isSelected
            ? 28
            : 12}
          cy={12}
          r={5}
          fill="white"
        />
        {isFocusVisible &&
          (
            <rect
              x={1}
              y={1}
              width={38}
              height={22}
              rx={11}
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

<Switch>
  Low power mode
</Switch>
```

## Usage[#](#usage)

---

The following examples show how to use the `Switch` component created in the above example.

### Default value[#](#default-value)

Switches are not selected by default. The `defaultSelected` prop can be used to set the default state.

```
<Switch defaultSelected>Wi-Fi</Switch>
```

```
<Switch defaultSelected>Wi-Fi</Switch>
```

```
<Switch
  defaultSelected
>
  Wi-Fi
</Switch>
```

### Controlled value[#](#controlled-value)

The `isSelected` prop can be used to make the selected state controlled. The `onChange` event is fired when the user presses the switch, and receives the new value.

```
function Example() {
  let [selected, setSelected] = React.useState(false);

  return (
    <>
      <Switch onChange={setSelected}>Low power mode</Switch>
      <p>{selected ? 'Low' : 'High'} power mode active.</p>
    </>
  );
}
```

```
function Example() {
  let [selected, setSelected] = React.useState(false);

  return (
    <>
      <Switch onChange={setSelected}>Low power mode</Switch>
      <p>{selected ? 'Low' : 'High'} power mode active.</p>
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
    false
  );

  return (
    <>
      <Switch
        onChange={setSelected}
      >
        Low power mode
      </Switch>
      <p>
        {selected
          ? 'Low'
          : 'High'}{' '}
        power mode
        active.
      </p>
    </>
  );
}
```

### Disabled[#](#disabled)

Switches can be disabled using the `isDisabled` prop.

```
<Switch isDisabled>Airplane Mode</Switch>
```

```
<Switch isDisabled>Airplane Mode</Switch>
```

```
<Switch isDisabled>
  Airplane Mode
</Switch>
```

### Read only[#](#read-only)

The `isReadOnly` prop makes the selection immutable. Unlike `isDisabled`, the Switch remains focusable.
See the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/readonly) for more information.

```
<Switch isSelected isReadOnly>Bluetooth</Switch>
```

```
<Switch isSelected isReadOnly>Bluetooth</Switch>
```

```
<Switch
  isSelected
  isReadOnly
>
  Bluetooth
</Switch>
```

### HTML forms[#](#html-forms)

Switch supports the `name` and `value` props for integration with HTML forms.

```
<Switch name="power" value="low">Low power mode</Switch>
```

```
<Switch name="power" value="low">Low power mode</Switch>
```

```
<Switch
  name="power"
  value="low"
>
  Low power mode
</Switch>
```

## Internationalization[#](#internationalization)

---

### RTL[#](#rtl)

In right-to-left languages, switches should be mirrored. The switch should be placed on the right
side of the label. Ensure that your CSS accounts for this.

| Name | Type | Description |
| --- | --- | --- |
| `children` | `ReactNode` | The content to render as the Switch's label. |
| `defaultSelected` | `boolean` | Whether the Switch should be selected (uncontrolled). |
| `isSelected` | `boolean` | Whether the Switch should be selected (controlled). |
| `onChange` | `( (isSelected: boolean )) => void` | Handler that is called when the Switch's selection state changes. |
| `value` | `string` | The value of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefvalue). |
| `isDisabled` | `boolean` | Whether the input is disabled. |
| `isReadOnly` | `boolean` | Whether the input can be selected but not changed by the user. |
| `autoFocus` | `boolean` | Whether the element should receive focus on render. |
| `onFocus` | `( (e: FocusEvent<Target> )) => void` | Handler that is called when the element receives focus. |
| `onBlur` | `( (e: FocusEvent<Target> )) => void` | Handler that is called when the element loses focus. |
| `onFocusChange` | `( (isFocused: boolean )) => void` | Handler that is called when the element's focus status changes. |
| `onKeyDown` | `( (e: KeyboardEvent )) => void` | Handler that is called when a key is pressed. |
| `onKeyUp` | `( (e: KeyboardEvent )) => void` | Handler that is called when a key is released. |
| `aria-controls` | `string` | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `excludeFromTabOrder` | `boolean` | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `name` | `string` | The name of the input element, used when submitting an HTML form. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#htmlattrdefname). |
| `form` | `string` | The `<form>` element to associate the input with. The value of this attribute must be the id of a `<form>` in the same document. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#form). |
| `aria-label` | `string` | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | Identifies the element (or elements) that provide a detailed, extended description for the object. |

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

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
| `isSelected` | `boolean` | Whether the switch is selected. |
| `isPressed` | `boolean` | Whether the switch is in a pressed state. |
| `isDisabled` | `boolean` | Whether the switch is disabled. |
| `isReadOnly` | `boolean` | Whether the switch is read only. |

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

Any focusable element, including both HTML and SVG elements.

**Extends**: `Element, HTMLOrSVGElement`