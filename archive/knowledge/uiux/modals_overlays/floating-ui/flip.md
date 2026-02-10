# flip

Source: https://floating-ui.com/docs/flip

---

# flip

Changes the placement of the floating element to keep it in view.

*Visibility Optimizer*

```
import {flip} from '@floating-ui/dom';
```

This prevents the floating element from overflowing along its
side axis by flipping it to the opposite side by default.

Scroll up

Floating

## [Usage](#usage)

```
computePosition(referenceEl, floatingEl, {
  middleware: [flip()],
});
```

## [Options](#options)

These are the options you can pass to `flip()`.

```
interface FlipOptions extends DetectOverflowOptions {
  mainAxis?: boolean;
  crossAxis?: boolean | 'alignment';
  fallbackAxisSideDirection?: 'none' | 'start' | 'end';
  flipAlignment?: boolean;
  fallbackPlacements?: Array<Placement>;
  fallbackStrategy?: 'bestFit' | 'initialPlacement';
}
```

### [`mainAxis`](#mainaxis)

default: `true`

This is the main axis in which overflow is checked to perform a
flip. By disabling this, it will ignore overflow.

- `y`-axis for `'top'` and `'bottom'` placements
- `x`-axis for `'left'` and `'right'` placements

```
flip({
  mainAxis: false,
});
```

Scroll up

I will ignore main axis overflow

### [`crossAxis`](#crossaxis)

default: `true`

This is the cross axis in which overflow is checked to perform a
flip, the axis perpendicular to `mainAxis`. By disabling
this, it will ignore overflow.

```
flip({
  crossAxis: false,
});
```

Scroll around

I will check cross axis overflow (default)

Scroll around

I will ignore cross axis overflow

### [`fallbackAxisSideDirection`](#fallbackaxissidedirection)

default: `'none'`

Whether to allow fallback to the opposite axis if no placements
along the preferred placement axis fit, and if so, which side
direction along that axis to choose. If necessary, it will
fallback to the other direction.

- `'none'` signals that no fallback to the opposite axis
  should take place.
- `'start'` represents `'top'` or `'left'`.
- `'end'` represents `'bottom'` or `'right'`.

For instance, by default, if the initial `placement` is
set to `'right'`, then the placements to try (in order) are:

`['right', 'left']`

On a narrow viewport, it’s possible or even likely that *neither*
of these will fit.

By specifying a string other than `'none'`, you allow
placements along the perpendicular axis of the initial placement
to be tried. The direction determines which side of placement is
tried first:

```
flip({
  fallbackAxisSideDirection: 'start',
});
```

The above results in: `['right', 'left', 'top', 'bottom']`.

```
flip({
  fallbackAxisSideDirection: 'end',
});
```

The above results in: `['right', 'left', 'bottom', 'top']`.

As an example, if you’d like a tooltip that has a placement of
`'right'` to be placed on top on mobile (assuming it doesn’t
fit), then you’d use `'start'`. For an interactive popover,
you likely want to use `'end'` so it’s placed on the bottom,
closer to the user’s fingers.

In each of the following demos, the `placement` is
`'right'`.

Scroll horizontally

`fallbackAxisSideDirection` has been set to 'none' (default)

Notice that it can overflow.

Scroll horizontally

`fallbackAxisSideDirection` has been set to 'start'

Notice that it prefers `top` if it doesn’t fit.

Scroll horizontally

`fallbackAxisSideDirection` has been set to 'end'

Notice that it prefers `bottom` if it doesn’t fit.

### [`flipAlignment`](#flipalignment)

default: `true`

When an alignment is specified, e.g. `'top-start'` instead
of just `'top'`, this will flip to `'top-end'` if
`start` doesn’t fit.

```
flip({
  flipAlignment: false,
});
```

When using this with the `shift()` middleware, ensure
`flip()` is placed **before** `shift()` in your
middleware array. This ensures the `flipAlignment` logic
can act before `shift()`’s does.

### [`fallbackPlacements`](#fallbackplacements)

default: `[oppositePlacement]`

This describes an **explicit** array of placements to try if the
initial `placement` doesn’t fit on the axes in which
overflow is checked.

```
flip({
  fallbackPlacements: ['right', 'bottom'],
});
```

In the above example, if `placement` is set to
`'top'`, then the placements to try (in order) are:

`['top', 'right', 'bottom']`

Scroll down

Floating

### [`fallbackStrategy`](#fallbackstrategy)

default: `'bestFit'`

When no placements fit, then you’ll want to decide what happens.
`'bestFit'` will use the placement which fits best on the
checked axes. `'initialPlacement'` will use the initial
`placement` specified.

```
flip({
  fallbackStrategy: 'initialPlacement',
});
```

### […detectOverflowOptions](#detectoverflowoptions)

All of [`detectOverflow`](/docs/detectOverflow#options)’s options
can be passed. For instance:

```
flip({
  padding: 5, // 0 by default
});
```

### [Deriving options from state](#deriving-options-from-state)

You can derive the options from the
[middleware lifecycle state](/docs/middleware#middlewarestate):

```
flip((state) => ({
  padding: state.rects.reference.width,
}));
```

## [Final placement](#final-placement)

The placement returned from the function is always the final one,
not necessarily the one you passed in as the “preferred” one.

```
computePosition(referenceEl, floatingEl, {
  placement: 'bottom',
  middleware: [flip()],
}).then(({placement}) => {
  console.log(placement); // 'top' or 'bottom'
});
```

## [Combining with `shift()`](#combining-with-shift)

When using `flip()` with `shift()` together, the
recommended configuration is as follows:

```
const middleware = [offset(5)];
const flipMiddleware = flip({
  // Ensure we flip to the perpendicular axis if it doesn't fit
  // on narrow viewports.
  crossAxis: 'alignment',
  fallbackAxisSideDirection: 'end', // or 'start'
});
const shiftMiddleware = shift();
 
// Prioritize flip over shift for edge-aligned placements only.
if (placement.includes('-')) {
  middleware.push(flipMiddleware, shiftMiddleware);
} else {
  middleware.push(shiftMiddleware, flipMiddleware);
}
```

This results in the most expected positioning when using both
middleware regardless of the placement used.

## [Conflict with `autoPlacement()`](#conflict-with-autoplacement)

`flip()` and `autoPlacement()` cannot be used together
inside the same middleware array; make sure you choose only one
of them to use.

The reason is they both try to perform work on the placement but
with opposing strategies. Therefore, they will continually try to
change the result or work of the other one, leading to a reset
loop.

- `flip()` uses a fallback “no space” strategy. Ensures the
  preferred placement is kept unless there is no space left.
- `autoPlacement()` uses a primary “most space” strategy.
  Always chooses the placement with the most space available.