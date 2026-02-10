# shift

Source: https://floating-ui.com/docs/shift

---

# shift

Shifts the floating element to keep it in view.

*Visibility Optimizer*

```
import {shift} from '@floating-ui/dom';
```

This prevents the floating element from overflowing along its
axis of alignment, thereby preserving the side it’s placed on.

Scroll horizontally

## [Usage](#usage)

```
computePosition(referenceEl, floatingEl, {
  middleware: [shift()],
});
```

## [Options](#options)

These are the options you can pass to `shift()`.

```
interface ShiftOptions extends DetectOverflowOptions {
  mainAxis?: boolean;
  crossAxis?: boolean;
  limiter?: {
    fn: (state: MiddlewareState) => Coords;
    options?: any;
  };
}
```

### [`mainAxis`](#mainaxis)

default: `true`

This is the main axis in which shifting is applied.

- `x`-axis for `'top'` and `'bottom'` placements
- `y`-axis for `'left'` and `'right'` placements

```
shift({
  mainAxis: false,
});
```

Scroll horizontally

A floating element that does not shift along the x-axis

### [`crossAxis`](#crossaxis)

default: `false`

This is the cross axis in which shifting is applied, the opposite
axis of `mainAxis`.

Enabling this can lead to the floating element **overlapping**
the reference element, which may not be desired and is often
replaced by the `flip()` middleware.

```
shift({
  crossAxis: true,
});
```

Scroll down

### [`limiter`](#limiter)

default: no-op

This accepts a function that **limits** the shifting done, in
order to prevent detachment or “overly-eager” behavior. The
behavior is to stop shifting once the opposite edges of the
elements are aligned.

```
import {shift, limitShift} from '@floating-ui/dom';
```

```
shift({
  limiter: limitShift(),
});
```

This function itself takes options.

#### [limitShift.mainAxis](#limitshiftmainaxis)

default: `true`

Whether to apply limiting on the main axis.

```
shift({
  limiter: limitShift({
    mainAxis: false,
  }),
});
```

#### [limitShift.crossAxis](#limitshiftcrossaxis)

default: `true`

Whether to apply limiting on the cross axis.

```
shift({
  limiter: limitShift({
    crossAxis: false,
  }),
});
```

#### [limitShift.offset](#limitshiftoffset)

default: `0`

This will offset when the limiting starts. A positive number will
start limiting earlier, while negative later.

```
shift({
  limiter: limitShift({
    // Start limiting 5px earlier
    offset: 5,
  }),
});
```

This can also take a function, which provides the
`Rect`s of each element to read their dimensions:

```
shift({
  limiter: limitShift({
    // Start limiting by the reference's width earlier
    offset: ({rects, placement}) => rects.reference.width,
  }),
});
```

You may also pass an object to configure both axes:

```
shift({
  limiter: limitShift({
    // object
    offset: {
      mainAxis: 10,
      crossAxis: 5,
    },
    // or a function which returns one
    offset: ({rects, placement}) => ({
      mainAxis: rects.reference.height,
      crossAxis: rects.floating.width,
    }),
  }),
});
```

### […detectOverflowOptions](#detectoverflowoptions)

All of [`detectOverflow`](/docs/detectOverflow#options)’s options
can be passed. For instance:

```
shift({
  padding: 5, // 0 by default
});
```

If you find the padding does not get applied on the right side,
see [Handling large content](/docs/misc#handling-large-content).

### [Deriving options from state](#deriving-options-from-state)

You can derive the options from the
[middleware lifecycle state](/docs/middleware#middlewarestate):

```
shift((state) => ({
  padding: state.rects.reference.width,
}));
```

## [Data](#data)

The following data is available in `middlewareData.shift`:

```
interface Data {
  x: number;
  y: number;
}
```

`x` and `y` represent how much the floating element
has been shifted along that axis. The values are offsets, and
therefore can be negative.