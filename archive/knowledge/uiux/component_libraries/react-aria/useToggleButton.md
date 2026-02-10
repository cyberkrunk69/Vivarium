# useToggleButton

Source: https://react-spectrum.adobe.com/react-aria/useToggleButton.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../ToggleButton).

# useToggleButton

Provides the behavior and accessibility implementation for a toggle button component.
ToggleButtons allow users to toggle a selection on or off, for example switching between two states or modes.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useToggleButton} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/button/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/button "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/button "View package")

## API[#](#api)

---

`useToggleButton(
props: AriaToggleButtonOptions<ElementType>,
state: ToggleState,
ref: RefObject<any>
): ToggleButtonAria<HTMLAttributes<any>>`

## Features[#](#features)

---

Toggle buttons are similar to action buttons, but support an additional selection state
that is toggled when a user presses the button. There is no built-in HTML element that
represents a toggle button, so React Aria implements it using ARIA attributes.

- Native HTML `<button>`, `<a>`, and custom element type support
- Exposed as a toggle button via ARIA
- Mouse and touch event handling, and press state management
- Keyboard focus management and cross browser normalization
- Keyboard event support for `Space` and `Enter` keys

## Anatomy[#](#anatomy)

---

Toggle buttons consist of a clickable area usually containing a textual label or an icon
that users can click to toggle a selection state. In addition, keyboard users may toggle
the state using the `Space` or `Enter` keys.

`useToggleButton` returns props to be spread onto the button element, along with a boolean indicating
whether the user is currently pressing the button:

| Name | Type | Description |
| --- | --- | --- |
| `isSelected` | `boolean` | Whether the button is selected. |
| `isDisabled` | `boolean` | Whether the button is disabled. |
| `buttonProps` | `T` | Props for the button element. |
| `isPressed` | `boolean` | Whether the button is currently pressed. |

Selection state is managed by the `useToggleState`
hook in `@react-stately/toggle`. The state object should be passed as an option to `useToggleButton`.

If a visual label is not provided (e.g. an icon only button), then an `aria-label` or
`aria-labelledby` prop must be passed to identify the button to assistive technology.

## Example[#](#example)

---

By default, `useToggleButton` assumes that you are using it with a native `<button>` element. You can use a custom
element type by passing the `elementType` prop to `useToggleButton`. See the [useButton](../Button/useButton.html#custom-element-type)
docs for an example of this.

The following example shows how to use the `useToggleButton` and `useToggleState` hooks to build a toggle button.
The toggle state is used to switch between a green and blue background when unselected and selected respectively.
In addition, the `isPressed` state is used to adjust the background to be darker when the user presses down on the button.

```
import {useToggleState} from 'react-stately';
import {useToggleButton} from 'react-aria';
import {useRef} from 'react';

function ToggleButton(props) {
  let ref = useRef<HTMLButtonElement | null>(null);
  let state = useToggleState(props);
  let { buttonProps, isPressed } = useToggleButton(props, state, ref);

  return (
    <button
      {...buttonProps}
      style={{
        background: isPressed
          ? state.isSelected ? 'darkgreen' : 'gray'
          : state.isSelected
          ? 'green'
          : 'lightgray',
        color: state.isSelected ? 'white' : 'black',
        padding: 10,
        fontSize: 16,
        userSelect: 'none',
        WebkitUserSelect: 'none',
        border: 'none'
      }}
      ref={ref}
    >
      {props.children}
    </button>
  );
}

<ToggleButton>Pin</ToggleButton>
```

```
import {useToggleState} from 'react-stately';
import {useToggleButton} from 'react-aria';
import {useRef} from 'react';

function ToggleButton(props) {
  let ref = useRef<HTMLButtonElement | null>(null);
  let state = useToggleState(props);
  let { buttonProps, isPressed } = useToggleButton(
    props,
    state,
    ref
  );

  return (
    <button
      {...buttonProps}
      style={{
        background: isPressed
          ? state.isSelected ? 'darkgreen' : 'gray'
          : state.isSelected
          ? 'green'
          : 'lightgray',
        color: state.isSelected ? 'white' : 'black',
        padding: 10,
        fontSize: 16,
        userSelect: 'none',
        WebkitUserSelect: 'none',
        border: 'none'
      }}
      ref={ref}
    >
      {props.children}
    </button>
  );
}

<ToggleButton>Pin</ToggleButton>
```

```
import {useToggleState} from 'react-stately';
import {useToggleButton} from 'react-aria';
import {useRef} from 'react';

function ToggleButton(
  props
) {
  let ref = useRef<
    | HTMLButtonElement
    | null
  >(null);
  let state =
    useToggleState(
      props
    );
  let {
    buttonProps,
    isPressed
  } = useToggleButton(
    props,
    state,
    ref
  );

  return (
    <button
      {...buttonProps}
      style={{
        background:
          isPressed
            ? state
                .isSelected
              ? 'darkgreen'
              : 'gray'
            : state
                .isSelected
            ? 'green'
            : 'lightgray',
        color:
          state
              .isSelected
            ? 'white'
            : 'black',
        padding: 10,
        fontSize: 16,
        userSelect:
          'none',
        WebkitUserSelect:
          'none',
        border: 'none'
      }}
      ref={ref}
    >
      {props.children}
    </button>
  );
}

<ToggleButton>
  Pin
</ToggleButton>
```

## Usage[#](#usage)

---

The following examples show how to use the `ToggleButton` component created in the above example.

### Controlled selection state[#](#controlled-selection-state)

A default selection state for a toggle button can be set using the `defaultSelected` prop, or controlled with the `isSelected` prop. The `onChange` event is fired when the user presses the button, toggling the boolean. See React's documentation on
[uncontrolled components](https://reactjs.org/docs/uncontrolled-components.html) for more info.

```
function Example() {
  let [isSelected, setSelected] = React.useState(false);

  return (
    <ToggleButton
      isSelected={isSelected}
      onChange={setSelected}
      aria-label="Star">
      â
    </ToggleButton>
  );
}
```

```
function Example() {
  let [isSelected, setSelected] = React.useState(false);

  return (
    <ToggleButton
      isSelected={isSelected}
      onChange={setSelected}
      aria-label="Star">
      â
    </ToggleButton>
  );
}
```

```
function Example() {
  let [
    isSelected,
    setSelected
  ] = React.useState(
    false
  );

  return (
    <ToggleButton
      isSelected={isSelected}
      onChange={setSelected}
      aria-label="Star"
    >
      â
    </ToggleButton>
  );
}
```

### Disabled[#](#disabled)

A `ToggleButton` can be disabled using the `isDisabled` prop.

```
<ToggleButton isDisabled>Pin</ToggleButton>
```

```
<ToggleButton isDisabled>Pin</ToggleButton>
```

```
<ToggleButton
  isDisabled
>
  Pin
</ToggleButton>
```

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `isSelected` | `boolean` | â | Whether the element should be selected (controlled). |
| `defaultSelected` | `boolean` | â | Whether the element should be selected (uncontrolled). |
| `onChange` | `( (isSelected: boolean )) => void` | â | Handler that is called when the element's selection state changes. |
| `isDisabled` | `boolean` | â | Whether the button is disabled. |
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
| `aria-disabled` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the element is disabled to users of assistive technology. |
| `aria-expanded` | `boolean |Â 'true' |Â 'false'` | â | Indicates whether the element, or another grouping element it controls, is currently expanded or collapsed. |
| `aria-haspopup` | `boolean |Â 'menu' |Â 'listbox' |Â 'tree' |Â 'grid' |Â 'dialog' |Â 'true' |Â 'false'` | â | Indicates the availability and type of interactive popup element, such as menu or dialog, that can be triggered by an element. |
| `aria-controls` | `string` | â | Identifies the element (or elements) whose contents or presence are controlled by the current element. |
| `aria-pressed` | `boolean |Â 'true' |Â 'false' |Â 'mixed'` | â | Indicates the current "pressed" state of toggle buttons. |
| `preventFocusOnPress` | `boolean` | â | Whether to prevent focus from moving to the button when pressing it.  Caution, this can make the button inaccessible and should only be used when alternative keyboard interaction is provided, such as ComboBox's MenuTrigger or a NumberField's increment/decrement control. |
| `excludeFromTabOrder` | `boolean` | â | Whether to exclude the element from the sequential tab order. If true, the element will not be focusable via the keyboard by tabbing. This should be avoided except in rare scenarios where an alternative means of accessing the element or its functionality via the keyboard is available. |
| `id` | `string` | â | The element's unique identifier. See [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id). |
| `aria-label` | `string` | â | Defines a string value that labels the current element. |
| `aria-labelledby` | `string` | â | Identifies the element (or elements) that labels the current element. |
| `aria-describedby` | `string` | â | Identifies the element (or elements) that describes the object. |
| `aria-details` | `string` | â | Identifies the element (or elements) that provide a detailed, extended description for the object. |
| `elementType` | `ElementType |Â JSXElementConstructor<any>` | `'button'` | The HTML element or React element used to render the button, e.g. 'div', 'a', or `RouterLink`. |

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
| `isSelected` | `boolean` | Whether the button is selected. |
| `isDisabled` | `boolean` | Whether the button is disabled. |
| `buttonProps` | `T` | Props for the button element. |
| `isPressed` | `boolean` | Whether the button is currently pressed. |

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