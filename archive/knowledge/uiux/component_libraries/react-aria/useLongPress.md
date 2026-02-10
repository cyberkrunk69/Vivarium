# useLongPress

Source: https://react-spectrum.adobe.com/react-aria/useLongPress.html

---

# useLongPress

Handles long press interactions across mouse and touch devices. Supports a customizable time threshold,
accessibility description, and normalizes behavior across browsers and devices.

Activate

```
import React from 'react';
import {mergeProps} from 'react-aria';
import {useLongPress, usePress} from '@react-aria/interactions';

function Example() {
  let [events, setEvents] = React.useState<string[]>([]);
  let [mode, setMode] = React.useState('Activate');

  // Long press to activate "Hyper speed"
  let {longPressProps} = useLongPress({
    accessibilityDescription: 'Long press to activate hyper speed',
    onLongPressStart: e => setEvents(
      events => [`long press start with ${e.pointerType}`, ...events]
    ),
    onLongPressEnd: e => setEvents(
      events => [`long press end with ${e.pointerType}`, ...events]
    ),
    onLongPress: e => {
      setMode('Hyper speed');
      setEvents(
        events => [`long press with ${e.pointerType}`, ...events]
      );
    }
  });

  // Short press to activate "Normal speed"
  let {pressProps} = usePress({
    onPress: e => {
      setMode('Normal speed');
      setEvents(
        events => [`press with ${e.pointerType}`, ...events]
      );
    }
  });

  return (
    <>
      <button {...mergeProps(pressProps, longPressProps)}>{mode}</button>
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

### Accessibility

This example does not have a keyboard accessible way to trigger the long press action. Because the method of triggeringthis action will differ depending on the component, it is outside the scope of `useLongPress`. Make sure to implement a keyboardfriendly alternative to all long press interactions if you are using this hook directly.

## Features

A long press is triggered when a user presses and holds their pointer over a target for a minimum period of time. If the user moves their pointer off of the target before the time threshold, the interaction is canceled. Once a long press event is triggered, other pointer interactions that may be active such as `usePress` and `useMove` will be canceled so that only the long press is activated.

- Handles mouse and touch events
- Prevents text selection on touch devices while long pressing
- Prevents browser and OS context menus from appearing while long pressing
- Customizable time threshold for long press
- Supports an accessibility description to indicate to assistive technology users that a long press action is available

## API

`useLongPress(props: LongPressProps): LongPressResult`

### LongPressProps

| Name | Type | Default |
| --- | --- | --- |
| `accessibilityDescription` | `string` | **Default:** â |
| A description for assistive techology users indicating that a long press action is available, e.g. "Long press to open menu". | | |
| `threshold` | `number` | **Default:** `500ms` |
| The amount of time in milliseconds to wait before triggering a long press. | | |
| `onLongPress` | `(e: LongPressEvent) => void` | **Default:** â |
| Handler that is called when the threshold time is met while the press is over the target. | | |
| `onLongPressEnd` | `(e: LongPressEvent) => void` | **Default:** â |
| Handler that is called when a long press interaction ends, either over the target or when the pointer leaves the target. | | |
| `onLongPressStart` | `(e: LongPressEvent) => void` | **Default:** â |
| Handler that is called when a long press interaction starts. | | |
| `isDisabled` | `boolean` | **Default:** â |
| Whether long press events should be disabled. | | |

### LongPressResult

| Name | Type |
| --- | --- |
| `longPressProps` | `DOMAttributes` |
| Props to spread on the target element. | | |

### LongPressEvent

Each of these handlers is fired with a `LongPressEvent`, which exposes information about the target and the
type of event that triggered the interaction.

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
| `type` | `'longpressstart' |Â 'longpressend' |Â 'longpress'` |
| The type of long press event being fired. | | |