# useFocusRing

Source: https://react-spectrum.adobe.com/react-aria/useFocusRing.html

---

# useFocusRing

Determines whether a focus ring should be shown to indicate keyboard focus.
Focus rings are visible only when the user is interacting with a keyboard,
not with a mouse, touch, or other input methods.

Test

```
import {useFocusRing} from 'react-aria';

function Example() {
  let {isFocusVisible, focusProps} = useFocusRing();

  return (
    <button
      {...focusProps}
      style={{
        WebkitAppearance: 'none',
        appearance: 'none',
        background: 'green',
        border: 'none',
        color: 'white',
        fontSize: 14,
        padding: '8px 12px',
        borderRadius: 8,
        outline: isFocusVisible ? '2px solid dodgerblue' : 'none',
        outlineOffset: 2
      }}>
      Test
    </button>
  );
}
```

Expand code

## Features

The `useFocusRing` hook returns whether a focus ring should be displayed to indicate keyboard focus for a component.
This helps keyboard users determine which element on a page or in an application has keyboard focus as they
navigate around. Focus rings are only visible when interacting with a keyboard so as not to distract mouse
and touch screen users.

If CSS classes are being used for styling, see the <FocusRing> component for a shortcut.

## API

`useFocusRing(props: AriaFocusRingProps): FocusRingAria`

### AriaFocusRingProps

| Name | Type | Default |
| --- | --- | --- |
| `autoFocus` | `boolean` | **Default:** â |
| Whether the element will be auto focused. | | |
| `isTextInput` | `boolean` | **Default:** â |
| Whether the element is a text input. | | |
| `within` | `boolean` | **Default:** `'false'` |
| Whether to show the focus ring when something inside the container element has focus (true), or only if the container itself has focus (false). | | |

### FocusRingAria

| Name | Type |
| --- | --- |
| `focusProps` | `DOMAttributes` |
| Props to apply to the container element with the focus ring. | | |
| `isFocusVisible` | `boolean` |
| Whether keyboard focus should be visible. | | |
| `isFocused` | `boolean` |
| Whether the element is currently focused. | | |