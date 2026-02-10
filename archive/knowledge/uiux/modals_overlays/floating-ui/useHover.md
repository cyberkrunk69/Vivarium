# useHover

Source: https://floating-ui.com/docs/useHover

---

# useHover

Opens the floating element while hovering over the reference
element, like CSS `:hover`.

```
import {useHover} from '@floating-ui/react';
```

Includes the ability to enter the floating element
[without it closing](/docs/useHover#safepolygon).

## [Usage](#usage)

This Hook returns event handler props.

To use it, pass it the `context` object returned from
`useFloating()` or
[`useFloatingRootContext`](/docs/useInteractions#external-reference),
and then feed its result into the `useInteractions()` array.
The returned prop getters are then spread onto the elements for
rendering.

```
function App() {
  const [isOpen, setIsOpen] = useState(false);
 
  const {refs, floatingStyles, context} = useFloating({
    open: isOpen,
    onOpenChange: setIsOpen,
  });
 
  const hover = useHover(context);
 
  const {getReferenceProps, getFloatingProps} = useInteractions([
    hover,
  ]);
 
  return (
    <>
      <div ref={refs.setReference} {...getReferenceProps()}>
        Reference element
      </div>
      {isOpen && (
        <div
          ref={refs.setFloating}
          style={floatingStyles}
          {...getFloatingProps()}
        >
          Floating element
        </div>
      )}
    </>
  );
}
```

## [Examples](#examples)

- [Default hover](https://codesandbox.io/s/late-https-lu3833?file=/src/App.tsx)

## [Props](#props)

```
interface UseHoverProps {
  enabled?: boolean;
  mouseOnly?: boolean;
  delay?: number | Partial<{open: number; close: number}>;
  restMs?: number;
  move?: boolean;
  handleClose?: null | HandleCloseFn;
}
```

### [`enabled`](#enabled)

default: `true`

Conditionally enable/disable the Hook.

```
useHover(context, {
  enabled: false,
});
```

This is also useful when you want to disable further events from
firing based on some condition. For example, you may disable the
hook after hovering over the floating element to then prevent it
from closing.

### [`mouseOnly`](#mouseonly)

default: `false`

Whether the logic only runs for mouse input, ignoring both touch
and pen pointer inputs.

```
useHover(context, {
  mouseOnly: true,
});
```

### [`delay`](#delay)

default: `0`

Waits for the specified time when the event listener runs before
changing the `open` state.

```
useHover(context, {
  // Delay opening or closing the floating element by 500ms.
  delay: 500,
 
  // Configure the delay for opening and closing separately.
  delay: {
    open: 500,
    close: 0,
  },
});
```

### [`restMs`](#restms)

default: `0` (off)

Waits until the user’s cursor is at “rest” over the reference
element before changing the open state.

```
useHover(context, {
  // The user's cursor must be at rest for 150ms before opening.
  restMs: 150,
});
```

You can also use a fallback delay if the user’s cursor never
rests, to ensure the floating element will eventually open:

```
useHover(context, {
  restMs: 150,
  // If their cursor never rests, open it after 1000ms as a
  // fallback.
  delay: {open: 1000},
});
```

### [`move`](#move)

default: `true`

Whether moving the cursor over the floating element will open it,
without a regular hover event required.

For example, if it was resting over the reference element when it
closed. Uses the `'mousemove'` event.

```
useHover(context, {
  move: false,
});
```

### [`handleClose`](#handleclose)

default: `null`

Accepts an event handler that runs on `mousemove` to
control when the floating element closes once the cursor leaves
the reference element.

The package exports a `safePolygon()` handler which will
only close the floating element if the pointer is outside a
dynamically computed polygon area. This allows the user to move
the cursor off the reference element and towards the floating
element without it closing (e.g. it has interactive content
inside).

```
import {useHover, safePolygon} from '@floating-ui/react';
 
useHover(context, {
  handleClose: safePolygon(),
});
```

This handler runs on `mousemove`.

For a simpler alternative, depending on the type of floating
element, you can use a short close delay instead.

## [safePolygon](#safepolygon)

A “safe” polygon is one that a pointer is safe to traverse as it
moves off the reference element and toward the floating element
after hovering it. If the pointer moves outside of this safe
area, the floating element closes.

It is a dynamic polygon (either a rect or a triangle) originating
from the cursor once it leaves a reference element. The triangle
looks like this:

[](/safe-polygon.mp4)

This function takes options.

### [`requireIntent`](#requireintent)

default: `true`

Determines whether intent is required for the triangle polygon to
be generated (that is, the cursor is moving quickly enough toward
the floating element). `false` will keep the triangle active
no matter the intent.

```
useHover(context, {
  handleClose: safePolygon({
    requireIntent: false,
  }),
});
```

When reference elements are placed near each other and they each
have a hoverable floating element attached, `true` ensures
that hover events for the other nearby references aren’t too
aggressively blocked.

### [`buffer`](#buffer)

default: `0.5`

Determines the amount of buffer (in pixels) there is around the
polygon.

While the default value should handle the vast majority of cases
correctly, if you find your floating element is closing
unexpectedly as the pointer tries to move toward the floating
element, try increasing this value.

```
useHover(context, {
  handleClose: safePolygon({
    buffer: 1,
  }),
});
```

#### [Ignoring the triangle](#ignoring-the-triangle)

If you only want the offset portion (rectangle bridge) between
the reference and floating elements to be considered, you can set
the value to `-Infinity`.

```
useHover(context, {
  handleClose: safePolygon({
    // Don't generate a triangle polygon, only consider the
    // rectangular bridge between the elements.
    buffer: -Infinity,
  }),
});
```

### [`blockPointerEvents`](#blockpointerevents)

default: `false`

Whether CSS `pointer-events` behind the polygon, reference, and
floating elements are blocked. This ensures the user does not
fire hover events over other elements unintentionally while they
traverse the polygon.

```
useHover(context, {
  handleClose: safePolygon({
    blockPointerEvents: true,
  }),
});
```

This can cause container elements that listen for `mouseleave`
events to fire. In older versions of Chrome (<114), scrolling
containers can’t be scrolled while the pointer is over the
floating element (the main window remains unaffected).

A `[data-floating-ui-safe-polygon]` selector is
available as a parent, so scrolling containers can negate the
`pointer-events` style:

```
[data-floating-ui-safe-polygon] .scroll {
  pointer-events: auto;
}
 
[data-floating-ui-safe-polygon] .scroll > div {
  pointer-events: none;
}
```

```
<div className="scroll">
  <div>
    Content inside here will remain blocked without affecting the
    scrolling parent.
  </div>
</div>
```