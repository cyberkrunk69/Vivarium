# useMove

Source: https://react-spectrum.adobe.com/react-aria/useMove.html

---

# useMove

Handles move interactions across mouse, touch, and keyboard, including dragging with
the mouse or touch, and using the arrow keys. Normalizes behavior across browsers and
platforms, and ignores emulated mouse events on touch devices.

```
import React from 'react';
import {useMove} from 'react-aria';

function Example() {
  const CONTAINER_SIZE = 200;
  const BALL_SIZE = 30;

  let [events, setEvents] = React.useState<string[]>([]);
  let [color, setColor] = React.useState('black');
  let [position, setPosition] = React.useState({
    x: 0,
    y: 0
  });

  let clamp = pos => Math.min(Math.max(pos, 0), CONTAINER_SIZE - BALL_SIZE);
  let {moveProps} = useMove({
    onMoveStart(e) {
      setColor('red');
      setEvents(events => [`move start with pointerType = ${e.pointerType}`, ...events]);
    },
    onMove(e) {
      setPosition(({x, y}) => {
        // Normally, we want to allow the user to continue
        // dragging outside the box such that they need to
        // drag back over the ball again before it moves.
        // This is handled below by clamping during render.
        // If using the keyboard, however, we need to clamp
        // here so that dragging outside the container and
        // then using the arrow keys works as expected.
        if (e.pointerType === 'keyboard') {
          x = clamp(x);
          y = clamp(y);
        }

        x += e.deltaX;
        y += e.deltaY;
        return {x, y};
      });

      setEvents(events => [`move with pointerType = ${e.pointerType}, deltaX = ${e.deltaX}, deltaY = ${e.deltaY}`, ...events]);
    },
    onMoveEnd(e) {
      setPosition(({x, y}) => {
        // Clamp position on mouse up
        x = clamp(x);
        y = clamp(y);
        return {x, y};
      });
      setColor('black');
      setEvents(events => [`move end with pointerType = ${e.pointerType}`, ...events]);
    }
  });

  return (
    <>
      <div
        style={{
          width: CONTAINER_SIZE,
          height: CONTAINER_SIZE,
          background: 'white',
          border: '1px solid black',
          position: 'relative',
          touchAction: 'none'
        }}>
        <div
          {...moveProps}
          tabIndex={0}
          style={{
            width: BALL_SIZE,
            height: BALL_SIZE,
            borderRadius: '100%',
            position: 'absolute',
            left: clamp(position.x),
            top: clamp(position.y),
            background: color
          }} />
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

Move events are emitted after the user presses down and then drags the pointer around. They specify the distance that the pointer traveled since the last event. In addition, after a user focuses the target element, move events are fired when the user presses the arrow keys.

- Handles mouse and touch events
- Handles arrow key presses
- Disables text selection while the user drags

## API

`useMove(props: MoveEvents): MoveResult`

### MoveEvents

| Name | Type |
| --- | --- |
| `onMoveEnd` | `(e: MoveEndEvent) => void` |
| Handler that is called when a move interaction ends. | | |
| `onMove` | `(e: MoveMoveEvent) => void` |
| Handler that is called when the element is moved. | | |
| `onMoveStart` | `(e: MoveStartEvent) => void` |
| Handler that is called when a move interaction starts. | | |

### MoveResult

| Name | Type |
| --- | --- |
| `moveProps` | `DOMAttributes` |
| Props to spread on the target element. | | |

### MoveEvent

| Name | Type |
| --- | --- |
| `altKey` | `boolean` |
| Whether the alt keyboard modifier was held during the move event. | | |
| `metaKey` | `boolean` |
| Whether the meta keyboard modifier was held during the move event. | | |
| `ctrlKey` | `boolean` |
| Whether the ctrl keyboard modifier was held during the move event. | | |
| `shiftKey` | `boolean` |
| Whether the shift keyboard modifier was held during the move event. | | |
| `pointerType` | `PointerType` |
| The pointer type that triggered the move event. | | |
| `deltaY` | `number` |
| The amount moved in the Y direction since the last event. | | |
| `deltaX` | `number` |
| The amount moved in the X direction since the last event. | | |
| `type` | `'move'` |
| The type of move event being fired. | | |