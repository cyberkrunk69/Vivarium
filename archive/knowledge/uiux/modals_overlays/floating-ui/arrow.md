# arrow

Source: https://floating-ui.com/docs/arrow

---

# arrow

Provides positioning data for an arrow element (triangle or
caret) inside the floating element, such that it appears to be
pointing toward the center of the reference element.

*Data Provider*

```
import {arrow} from '@floating-ui/dom';
```

This is useful to add an additional visual cue to the floating
element about which element it is referring to.

Scroll horizontally

## [Usage](#usage)

The layout box of the arrow element should be a square with equal
width and height. Inner or pseudo-elements may have a different
aspect ratio.

Given an arrow element inside your floating element:

```
<div>
  Floating element
  <div id="arrow"></div>
</div>
```

```
#arrow {
  position: absolute;
}
```

Pass the element to the
`arrow()` middleware and assign the dynamic styles using the
coordinates data available in `middlewareData.arrow`:

```
const arrowEl = document.querySelector('#arrow');
 
computePosition(referenceEl, floatingEl, {
  middleware: [arrow({element: arrowEl})],
}).then(({middlewareData}) => {
  if (middlewareData.arrow) {
    const {x, y} = middlewareData.arrow;
 
    Object.assign(arrowEl.style, {
      left: x != null ? `${x}px` : '',
      top: y != null ? `${y}px` : '',
    });
  }
});
```

This middleware is designed only to position the arrow on one
axis (`x` for `'top'` or `'bottom'` placements). The
other axis is considered “static”, which means it does not need
to be positioned dynamically.

You may however want to position **both** axes statically in the
following scenario:

- The reference element is either wider or taller than the
  floating element;
- The floating element is using an edge alignment
  (`-start` or `-end` placement).

## [Visualization](#visualization)

To help you understand how this middleware works, here is a
[visualization tutorial on CodeSandbox](https://codesandbox.io/s/mystifying-kare-ee3hmh?file=/src/index.js).

## [Order](#order)

`arrow()` should generally be placed toward the end of your
middleware array, after `shift()` or `autoPlacement()` (if used).

## [Placement](#placement)

To know which side the floating element is actually placed at for
the static axis offset of the arrow, the placement is returned:

```
computePosition(referenceEl, floatingEl, {
  placement: 'top',
  middleware: [flip(), arrow({element: arrowEl})],
}).then((data) => {
  // The final placement can be 'bottom' or 'top'
  const placement = data.placement;
});
```

## [Options](#options)

These are the options you can pass to `arrow()`.

```
interface ArrowOptions {
  element: Element;
  padding?: Padding;
}
```

### [`element`](#element)

default: `undefined`

This is the arrow element to be positioned, which must be a child
of the floating element.

```
arrow({
  element: document.querySelector('#arrow'),
});
```

### [`padding`](#padding)

default: `0`

This describes the padding between the arrow and the edges of the
floating element. If your floating element has
`border-radius`, this will prevent it from
overflowing the corners.

```
arrow({
  padding: 5, // stop 5px from the edges of the floating element
});
```

### [Deriving options from state](#deriving-options-from-state)

You can derive the options from the
[middleware lifecycle state](/docs/middleware#middlewarestate):

```
arrow((state) => ({
  padding: state.rects.reference.width,
}));
```

## [Data](#data)

The following data is available in `middlewareData.arrow`:

```
interface Data {
  x?: number;
  y?: number;
  centerOffset: number;
}
```

### [`x`](#x)

This property exists if the arrow should be offset on the x-axis.

### [`y`](#y)

This property exists if the arrow should be offset on the y-axis.

### [`centerOffset`](#centeroffset)

This property describes where the arrow actually is relative to
where it could be if it were allowed to overflow the floating
element in order to stay centered to the reference element.

This enables two useful things:

- You can hide the arrow if it can’t stay centered to the
  reference, i.e. `centerOffset !== 0`.
- You can interpolate the shape of the arrow (e.g. skew it) so it
  stays centered as best as possible.