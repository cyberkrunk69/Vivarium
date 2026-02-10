# inline

Source: https://floating-ui.com/docs/inline

---

# inline

Improves positioning for inline reference elements that span over
multiple lines.

*Placement Modifier*

```
import {inline} from '@floating-ui/dom';
```

This is useful for reference elements such as hyperlinks or range
selections, as the default positioning using
`getBoundingClientRect()` may appear “detached” when
measuring over the bounding box.

In the following examples, the `placement` is
`'top'`.

Without `inline()`:

![inline disabled](/inline-disabled.png)

With `inline()`:

![inline enabled](/inline-enabled.png)

## [Usage](#usage)

```
computePosition(referenceEl, floatingEl, {
  middleware: [inline()],
});
```

### [Choosing a rect](#choosing-a-rect)

By default, `inline()` infers which of the
`ClientRect`s to choose based on the `placement`.
However, you may want a different rect to be chosen.

For instance, if the user hovered over the last client rect, you
likely want the floating element to be placed there. This logic
is only applied when the reference element’s rects are disjoined.

```
function onMouseEnter({clientX: x, clientY: y}) {
  computePosition(referenceEl, floatingEl, {
    middleware: [inline({x, y})],
  }).then(({x, y}) => {
    // ...
  });
}
 
referenceEl.addEventListener('mouseenter', onMouseEnter);
```

## [Order](#order)

`inline()` should generally be placed toward the beginning
of your middleware array, before `flip()` (if used).

## [Options](#options)

These are the options you can pass to `inline()`.

```
interface InlineOptions {
  x?: number;
  y?: number;
  padding?: number | SideObject;
}
```

### [`x`](#x)

default: `undefined`

This is the viewport-relative (client) x-axis coordinate which
can be passed in to choose a rect.

### [`y`](#y)

default: `undefined`

This is the viewport-relative (client) y-axis coordinate which
can be passed in to choose a rect.

### [`padding`](#padding)

default: `2`

This describes the padding around a disjoined rect when choosing
it.

### [Deriving options from state](#deriving-options-from-state)

You can derive the options from the
[middleware lifecycle state](/docs/middleware#middlewarestate):

```
inline((state) => ({
  padding: state.rects.reference.width,
}));
```