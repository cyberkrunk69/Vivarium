# useHover

Source: https://react-spectrum.adobe.com/react-aria/useHover.html

---

# useHover

Handles pointer hover interactions for an element. Normalizes behavior
across browsers and platforms, and ignores emulated mouse events on touch devices.

Hover me!

```
import React from 'react';
import {useHover} from 'react-aria';

function Example() {
  let [events, setEvents] = React.useState<string[]>([]);
  let {hoverProps, isHovered} = useHover({
    onHoverStart: e => setEvents(
      events => [...events, `hover start with ${e.pointerType}`]
    ),
    onHoverEnd: e => setEvents(
      events => [...events, `hover end with ${e.pointerType}`]
    )
  });

  return (
    <>
      <div
        {...hoverProps}
        style={{
          background: isHovered ? 'darkgreen' : 'green',
          color: 'white',
          display: 'inline-block',
          padding: '8px 12px',
          borderRadius: 8,
          cursor: 'pointer'
        }}
        role="button"
        tabIndex={0}>
        Hover me!
      </div>
      <ul
        style={{
          maxHeight: '200px',
          overflow: 'auto'
        }}>
        {events.map((e, i) => <li key={i}>{e}</li>)}
      </ul>
    </>
  );
}
```

Expand code

## Features

`useHover` is similar to the [:hover](https://developer.mozilla.org/en-US/docs/Web/CSS/:hover) CSS pseudo class, but only applies on mouse interactions. `:hover` is sticky on touch devices, applying continuously until the user interacts with another element, and on devices with both mouse and touch support there is no CSS-only way to apply hover states only when interacting with a pointer. Read our [blog post](blog/building-a-button-part-2) to learn more.

### Accessibility

Hover interactions should never be the only way to interact with an element because they are notsupported across all devices. Alternative interactions should be provided on touch devices, forexample a long press or an explicit button to tap.

## API

`useHover(props: HoverProps): HoverResult`

### HoverProps

| Name | Type |
| --- | --- |
| `onHoverChange` | `(isHovering: boolean) => void` |
| Handler that is called when the hover state changes. | | |
| `onHoverEnd` | `(e: HoverEvent) => void` |
| Handler that is called when a hover interaction ends. | | |
| `onHoverStart` | `(e: HoverEvent) => void` |
| Handler that is called when a hover interaction starts. | | |
| `isDisabled` | `boolean` |
| Whether the hover events should be disabled. | | |

### HoverResult

| Name | Type |
| --- | --- |
| `isHovered` | `boolean` |
| `hoverProps` | `DOMAttributes` |
| Props to spread on the target element. | | |

### HoverEvent

| Name | Type |
| --- | --- |
| `target` | `HTMLElement` |
| The target element of the hover event. | | |
| `pointerType` | `'mouse' |Â 'pen'` |
| The pointer type that triggered the hover event. | | |
| `type` | `'hoverstart' |Â 'hoverend'` |
| The type of hover event being fired. | | |