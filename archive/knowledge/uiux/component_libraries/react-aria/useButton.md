# useButton

Source: https://react-spectrum.adobe.com/react-aria/useButton.html

---

### Migration in progress

This page is still being migrated to our new website. In the meantime, you can explore the new React Aria Components docs [here](../Button).

# useButton

Provides the behavior and accessibility implementation for a button component. Handles mouse, keyboard, and touch interactions,
focus behavior, and ARIA props for both native button elements and custom element types.

|  |  |
| --- | --- |
| install | `yarn add react-aria` |
| version | 3.45.0 |
| usage | `import {useButton} from 'react-aria'` |

[View ARIA pattern

W3C](https://www.w3.org/WAI/ARIA/apg/patterns/button/ "View ARIA pattern")[View repository

GitHub](https://github.com/adobe/react-spectrum/tree/main/packages/@react-aria/button "View repository")[View package

NPM](https://www.npmjs.com/package/@react-aria/button "View package")

## API[#](#api)

---

`useButton(
(props: AriaButtonOptions<ElementType>,
, ref: RefObject<any>
)): ButtonAria<HTMLAttributes<any>>`

## Features[#](#features)

---

On the surface, building a custom styled button seems simple. However, there are many
cross browser inconsistencies in interactions and accessibility features to consider.
`useButton` handles all of these interactions for you, so you can focus on the styling.

- Native HTML `<button>` support
- `<a>` and custom element type support via ARIA
- Mouse and touch event handling, and press state management
- Keyboard focus management and cross browser normalization
- Keyboard event support for `Space` and `Enter` keys

Read our [blog post](../blog/building-a-button-part-1) about the complexities of building buttons that work well across devices and interaction methods.

## Anatomy[#](#anatomy)

---

Buttons consist of a clickable area usually containing a textual label or an icon
that users can click to perform an action. In addition, keyboard users may activate
buttons using the `Space` or `Enter` keys.

If a visual label is not provided (e.g. an icon only button), then an `aria-label` or
`aria-labelledby` prop must be passed to identify the button to assistive technology.

## Example[#](#example)

---

By default, `useButton` assumes that you are using it with a native `<button>` element.

```
import {useButton} from 'react-aria';
import {useRef} from 'react';

function Button(props) {
  let ref = useRef<HTMLButtonElement | null>(null);
  let { buttonProps } = useButton(props, ref);
  let { children } = props;

  return (
    <button {...buttonProps} ref={ref}>
      {children}
    </button>
  );
}

<Button onPress={() => alert('Button pressed!')}>Test</Button>
```

```
import {useButton} from 'react-aria';
import {useRef} from 'react';

function Button(props) {
  let ref = useRef<HTMLButtonElement | null>(null);
  let { buttonProps } = useButton(props, ref);
  let { children } = props;

  return (
    <button {...buttonProps} ref={ref}>
      {children}
    </button>
  );
}

<Button onPress={() => alert('Button pressed!')}>
  Test
</Button>
```

```
import {useButton} from 'react-aria';
import {useRef} from 'react';

function Button(props) {
  let ref = useRef<
    | HTMLButtonElement
    | null
  >(null);
  let { buttonProps } =
    useButton(
      props,
      ref
    );
  let { children } =
    props;

  return (
    <button
      {...buttonProps}
      ref={ref}
    >
      {children}
    </button>
  );
}

<Button
  onPress={() =>
    alert(
      'Button pressed!'
    )}
>
  Test
</Button>
```

## Custom element type[#](#custom-element-type)

---

Sometimes you might need to use an element other than a native `<button>`. `useButton` supports
this via the `elementType` prop. When used with an element other than a native button, `useButton`
automatically applies the necessary ARIA roles and attributes to ensure that the element is exposed
to assistive technology as a button.

In addition, this example shows usage of the `isPressed` value returned by `useButton` to properly
style the button's active state. You could use the CSS `:active` pseudo class for this, but `isPressed`
properly handles when the user drags their pointer off of the button, along with keyboard support and better
touch screen support.

```
function Button(props) {
  let { children } = props;
  let ref = useRef<HTMLButtonElement | null>(null);
  let { buttonProps, isPressed } = useButton({
    ...props,
    elementType: 'span'
  }, ref);

  return (
    <span
      {...buttonProps}
      style={{
        background: isPressed ? 'darkgreen' : 'green',
        color: 'white',
        padding: 10,
        cursor: 'pointer',
        userSelect: 'none',
        WebkitUserSelect: 'none'
      }}
      ref={ref}
    >
      {children}
    </span>
  );
}

<Button onPress={() => alert('Button pressed!')}>Test</Button>
```

```
function Button(props) {
  let { children } = props;
  let ref = useRef<HTMLButtonElement | null>(null);
  let { buttonProps, isPressed } = useButton({
    ...props,
    elementType: 'span'
  }, ref);

  return (
    <span
      {...buttonProps}
      style={{
        background: isPressed ? 'darkgreen' : 'green',
        color: 'white',
        padding: 10,
        cursor: 'pointer',
        userSelect: 'none',
        WebkitUserSelect: 'none'
      }}
      ref={ref}
    >
      {children}
    </span>
  );
}

<Button onPress={() => alert('Button pressed!')}>
  Test
</Button>
```

```
function Button(props) {
  let { children } =
    props;
  let ref = useRef<
    | HTMLButtonElement
    | null
  >(null);
  let {
    buttonProps,
    isPressed
  } = useButton({
    ...props,
    elementType: 'span'
  }, ref);

  return (
    <span
      {...buttonProps}
      style={{
        background:
          isPressed
            ? 'darkgreen'
            : 'green',
        color: 'white',
        padding: 10,
        cursor:
          'pointer',
        userSelect:
          'none',
        WebkitUserSelect:
          'none'
      }}
      ref={ref}
    >
      {children}
    </span>
  );
}

<Button
  onPress={() =>
    alert(
      'Button pressed!'
    )}
>
  Test
</Button>
```

## Usage[#](#usage)

---

The following examples show how to use the `Button` component created in the above example.

### Events[#](#events)

`useButton` supports user interactions via mouse, keyboard, and touch. You can handle all of these via the `onPress` prop. This is similar to the standard `onClick` event, but normalized to support all interaction methods equally. In addition, the `onPressStart`, `onPressEnd`, and `onPressChange` events are fired as the user interacts with the button.

Each of these handlers receives a `PressEvent`, which exposes information about the target and the type of event that triggered the interaction. See [usePress](../usePress) for more details.

```
function Example() {
  let [pointerType, setPointerType] = React.useState(null);

  return (
    <>
      <Button
        onPressStart={(e) => setPointerType(e.pointerType)}
        onPressEnd={(e) => setPointerType(null)}
      >
        Press me
      </Button>
      <p>
        {pointerType
          ? `You are pressing the button with a ${pointerType}!`
          : 'Ready to be pressed.'}
      </p>
    </>
  );
}
```

```
function Example() {
  let [pointerType, setPointerType] = React.useState(null);

  return (
    <>
      <Button
        onPressStart={(e) => setPointerType(e.pointerType)}
        onPressEnd={(e) => setPointerType(null)}
      >
        Press me
      </Button>
      <p>
        {pointerType
          ? `You are pressing the button with a ${pointerType}!`
          : 'Ready to be pressed.'}
      </p>
    </>
  );
}
```

```
function Example() {
  let [
    pointerType,
    setPointerType
  ] = React.useState(
    null
  );

  return (
    <>
      <Button
        onPressStart={(e) =>
          setPointerType(
            e.pointerType
          )}
        onPressEnd={(e) =>
          setPointerType(
            null
          )}
      >
        Press me
      </Button>
      <p>
        {pointerType
          ? `You are pressing the button with a ${pointerType}!`
          : 'Ready to be pressed.'}
      </p>
    </>
  );
}
```

### Disabled[#](#disabled)

A `Button` can be disabled using the `isDisabled` prop.

```
<Button isDisabled>Pin</Button>
```

```
<Button isDisabled>Pin</Button>
```

```
<Button isDisabled>
  Pin
</Button>
```

| Name | Type | Default | Description |
| --- | --- | --- | --- |
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

`BaseEvent<ReactKeyboardEvent<any>>`

`SyntheticEvent &Â {

stopPropagation: () => void,

continuePropagation: () => void

}`

| Name | Type | Description |
| --- | --- | --- |
| `buttonProps` | `T` | Props for the button element. |
| `isPressed` | `boolean` | Whether the button is currently pressed. |