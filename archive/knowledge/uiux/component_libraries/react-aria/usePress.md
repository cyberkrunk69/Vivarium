# usePress

Source: https://react-spectrum.adobe.com/react-aria/usePress.html

---

# usePress

Handles press interactions across mouse, touch, keyboard, and screen readers.
It normalizes behavior across browsers and platforms, and handles many nuances
of dealing with pointer and keyboard events.

Press me!

```
import React from 'react';
import {usePress} from 'react-aria';

function Example() {
  let [events, setEvents] = React.useState<string[]>([]);
  let {pressProps, isPressed} = usePress({
    onPressStart: e => setEvents(
      events => [...events, `press start with ${e.pointerType}`]
    ),
    onPressEnd: e => setEvents(
      events => [...events, `press end with ${e.pointerType}`]
    ),
    onPress: e => setEvents(
      events => [...events, `press with ${e.pointerType}`]
    )
  });

  return (
    <>
      <div
        {...pressProps}
        style={{
          background: isPressed ? 'darkgreen' : 'green',
          color: 'white',
          display: 'inline-block',
          padding: '8px 12px',
          borderRadius: 8,
          cursor: 'pointer'
        }}
        role="button"
        tabIndex={0}>
        Press me!
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

`usePress` returns the current press state, which can be used to adjust the visual appearance of the target. If the pointer is released over the target, then an `onPress` event is fired.

- Handles mouse and touch events
- Handles `Enter` or `Space` key presses
- Handles screen reader virtual clicks
- Normalizes focus behavior on mouse and touch interactions across browsers
- Disables text selection while the press interaction is active
- Cancels press interactions on scroll
- Normalizes many cross browser inconsistencies

Read our [blog post](blog/building-a-button-part-1) learn more.

## API

`usePress(props: PressHookProps): PressResult`

### PressEvents

| Name | Type |
| --- | --- |
| `onClick` | `(e: MouseEvent<FocusableElement>) => void` |
| **Not recommended â use `onPress` instead.** `onClick` is an alias for `onPress` provided for compatibility with other libraries. `onPress` provides additional event details for non-mouse interactions. | | |
| `onPressUp` | `(e: PressEvent) => void` |
| Handler that is called when a press is released over the target, regardless of whether it started on the target or not. | | |
| `onPressChange` | `(isPressed: boolean) => void` |
| Handler that is called when the press state changes. | | |
| `onPressEnd` | `(e: PressEvent) => void` |
| Handler that is called when a press interaction ends, either over the target or when the pointer leaves the target. | | |
| `onPressStart` | `(e: PressEvent) => void` |
| Handler that is called when a press interaction starts. | | |
| `onPress` | `(e: PressEvent) => void` |
| Handler that is called when the press is released over the target. | | |

### PressResult

| Name | Type |
| --- | --- |
| `pressProps` | `DOMAttributes` |
| Props to spread on the target element. | | |
| `isPressed` | `boolean` |
| Whether the target is currently pressed. | | |

### PressEvent

### Properties

| Name | Type |
| --- | --- |
| `y` | `number` |
| Y position relative to the target. | | |
| `x` | `number` |
| X position relative to the target. | | |
| `altKey` | `boolean` |
| Whether the alt keyboard modifier was held during the press event. | | |
| `metaKey` | `boolean` |
| Whether the meta keyboard modifier was held during the press event. | | |
| `ctrlKey` | `boolean` |
| Whether the ctrl keyboard modifier was held during the press event. | | |
| `shiftKey` | `boolean` |
| Whether the shift keyboard modifier was held during the press event. | | |
| `target` | `Element` |
| The target element of the press event. | | |
| `pointerType` | `PointerType` |
| The pointer type that triggered the press event. | | |
| `type` | `'pressstart' |Â 'pressend' |Â 'pressup' |Â 'press'` |
| The type of press event being fired. | | |

### Methods

|  |
| --- |
| `continuePropagation(): void` |
| By default, press events stop propagation to parent elements. In cases where a handler decides not to handle a specific event, it can call `continuePropagation()` to allow a parent to handle it. | | |