# computePosition

Source: https://floating-ui.com/docs/computePosition

---

# computePosition

Computes coordinates to position a floating element next to
another element.

```
import {computePosition} from '@floating-ui/dom';
```

## [Usage](#usage)

At its most basic, the function accepts two elements:

- **Reference element** — also known as the anchor element, this
  is the element that is being *referred* to for positioning.
  Often this is a button that triggers a floating popover like a
  tooltip or menu.
- **Floating element** — this is the element that floats next to
  the reference element, remaining anchored to it. This is the
  popover or tooltip itself.

```
<button id="button">My reference element</button>
<div id="tooltip">My floating element</div>
```

First, give the floating element initial CSS styles so that it
becomes an absolutely-positioned element that floats on top of
the UI with layout ready for being measured:

```
#tooltip {
  /* Float on top of the UI */
  position: absolute;
 
  /* Avoid layout interference */
  width: max-content;
  top: 0;
  left: 0;
}
```

Then, ensuring that these two elements are rendered onto the
document and **can be measured**, call `computePosition()`
with them as arguments.

The first argument is the reference
element to anchor to, and the second argument is
the floating element to be
positioned.

```
import {computePosition} from '@floating-ui/dom';
 
const button = document.querySelector('#button');
const tooltip = document.querySelector('#tooltip');
 
computePosition(button, tooltip).then(({x, y}) => {
  Object.assign(tooltip.style, {
    left: `${x}px`,
    top: `${y}px`,
  });
});
```

`computePosition()` returns a `Promise` that
resolves with the coordinates that can be used to apply styles to
the floating element.

By default, the floating element will be placed at the bottom
center of the reference element.

### [Measurable elements](#measurable-elements)

In order for the floating element to be measured and thus
correctly positioned, it must be rendered onto the DOM and not
hidden when `computePosition()` is called. Ensure CSS like
`display: none` is removed prior to calling the function.

### [Initial layout](#initial-layout)

To ensure positioning works smoothly, the dimensions of the
floating element should not change before and after being
positioned.

Certain CSS styles must be applied **before**
`computePosition()` is called:

```
#floating {
  position: absolute;
  width: max-content;
  top: 0;
  left: 0;
}
```

- `position: absolute`

This makes the element float on top of the UI with intrinsic
dimensions based on the content, instead of acting as a block.
The `top` and `left` coordinates can then take
effect.

- `width: max-content` (or a fixed value)
- `top: 0`
- `left: 0`

These properties prevent the floating element from resizing when
it overflows a container, removing layout interference that can
cause incorrect measurements.

This lets you place the floating element anywhere in the DOM tree
and have it be positioned correctly, regardless of the CSS styles
of any ancestor containers.

## [Anchoring](#anchoring)

Since `computePosition()` is only a single function call, it
only positions the floating element once.

To ensure it remains anchored to the reference element in a
variety of scenarios, such as when resizing or scrolling, wrap
the calculation in [`autoUpdate`](/docs/autoUpdate):

```
import {computePosition, autoUpdate} from '@floating-ui/dom';
 
// When the floating element is mounted to the DOM:
const cleanup = autoUpdate(referenceEl, floatingEl, () => {
  computePosition(referenceEl, floatingEl).then(({x, y}) => {
    // ...
  });
});
 
// ...later, when it's removed from the DOM:
cleanup();
```

## [Options](#options)

Passed as a third argument, this is the object to configure the
behavior.

```
computePosition(referenceEl, floatingEl, {
  // options
});
```

### [`placement`](#placement)

Where to place the floating element relative to its reference
element. By default, this is `'bottom'`.

12 strings are available:

```
type Placement =
  | 'top'
  | 'top-start'
  | 'top-end'
  | 'right'
  | 'right-start'
  | 'right-end'
  | 'bottom'
  | 'bottom-start'
  | 'bottom-end'
  | 'left'
  | 'left-start'
  | 'left-end';
```

```
computePosition(referenceEl, floatingEl, {
  placement: 'bottom-start', // 'bottom' by default
});
```

The `-start` and `-end` alignments are
[logical](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties)
and will adapt to the writing direction (e.g. RTL) as expected.

### [`strategy`](#strategy)

This is the type of CSS position property to use. Two strings are
available:

```
type Strategy = 'absolute' | 'fixed';
```

```
computePosition(referenceEl, floatingEl, {
  strategy: 'fixed', // 'absolute' by default
});
```

Ensure your initial layout matches the strategy:

```
#tooltip {
  position: fixed;
}
```

These strategies are differentiated as follows:

- `'absolute'` — the floating element is positioned relative
  to its nearest positioned ancestor. With most layouts, this
  usually requires the browser to do the least work when updating
  the position.
- `'fixed'` — the floating element is positioned relative to
  its nearest containing block (usually the viewport). This is
  useful when the reference element is also fixed to reduce
  jumpiness with positioning while scrolling. It will in many
  cases also
  [“break” the floating element out of a clipping ancestor](/docs/misc#clipping).

### [`middleware`](#middleware)

When you want granular control over how the floating element is
positioned, middleware are used. They read the current
coordinates, optionally alter them, and/or provide data for
rendering. They compose and work together to produce the final
coordinates which you receive as `x` and `y`
parameters.

The following are included in the package:

#### [Placement modifiers](#placement-modifiers)

These middleware alter the base placement coordinates.

- [`offset`](/docs/offset) modifies the placement to add distance
  or margin between the reference and floating elements.
- [`inline`](/docs/inline) positions the floating element
  relative to individual client rects rather than the bounding
  box for better precision.

#### [Visibility optimizers](#visibility-optimizers)

These middleware alter the coordinates to ensure the floating
element stays on screen optimally.

- [`shift`](/docs/shift) prevents the floating element from
  overflowing a clipping container by shifting it to stay in
  view.
- [`flip`](/docs/flip) prevents the floating element from
  overflowing a clipping container by flipping it to the opposite
  placement to stay in view.
- [`autoPlacement`](/docs/autoPlacement) automatically chooses a
  placement for you using a “most space” strategy.
- [`size`](/docs/size) resizes the floating element, for example
  so it will not overflow a clipping container, or to match the
  width of the reference element.

#### [Data providers](#data-providers)

These middleware only provide data and do not alter the
coordinates.

- [`arrow`](/docs/arrow) provides data to position an inner
  element of the floating element such that it is centered to its
  reference element.
- [`hide`](/docs/hide) provides data to hide the floating element
  in applicable situations when it no longer appears attached to
  its reference element due to different clipping contexts.

#### [Custom](#custom)

You can also craft your own custom middleware to extend the
behavior of the library. Read [Middleware](/docs/middleware) to
learn how to create your own.

#### [Conditional](#conditional)

Middleware can be called conditionally inside the array inline
for ergonomics:

```
// The array can accept `false`, `null`, or `undefined`
// inside of it. They get filtered out.
type MiddlewareOption = Array<
  Middleware | false | null | undefined
>;
```

Often this is useful for higher-level wrapper functions to avoid
needing the consumer to import middleware themselves:

```
function wrapper(referenceEl, floatingEl, options) {
  return computePosition(referenceEl, floatingEl, {
    ...options,
    middleware: [
      options.enableFlip && flip(),
      options.arrowEl && arrow({element: options.arrowEl}),
    ],
  });
}
```

## [Return value](#return-value)

`computePosition()` returns the following type:

```
interface ComputePositionReturn {
  x: number;
  y: number;
  placement: Placement;
  strategy: Strategy;
  middlewareData: MiddlewareData;
}
```

### [`x`](#x)

The x-coordinate of the floating element.

### [`y`](#y)

The y-coordinate of the floating element.

### [`placement`](#placement-1)

The final placement of the floating element, which may be
different from the initial or preferred one passed in due to
middleware modifications. This allows you to know which side the
floating element is placed at.

### [`strategy`](#strategy-1)

The CSS position property to use.

### [`middlewareData`](#middlewaredata)

The data returned by any middleware used.