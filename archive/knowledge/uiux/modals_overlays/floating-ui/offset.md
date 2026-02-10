# offset

Source: https://floating-ui.com/docs/offset

---

# offset

Translates the floating element along the specified axes.

*Placement Modifier*

```
import {offset} from '@floating-ui/dom';
```

This lets you add distance (margin or spacing) between the
reference and floating element, slightly alter the placement, or
even create
[custom placements](/docs/offset#creating-custom-placements).

0px

Floating

10px

Floating

## [Usage](#usage)

```
computePosition(referenceEl, floatingEl, {
  middleware: [offset(10)],
});
```

The value(s) passed are
[logical](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties),
meaning their effect on the physical result is dependent on the
placement, writing direction (e.g. RTL), or alignment.

## [Order](#order)

`offset()` should generally be placed at the beginning of
your middleware array.

## [Options](#options)

These are the options you can pass to `offset()`.

```
type Options =
  | number
  | {
      mainAxis?: number;
      crossAxis?: number;
      alignmentAxis?: number | null;
    };
```

A number represents the distance (gutter or margin) between the
floating element and the reference element. This is shorthand for
`mainAxis`.

```
offset(10);
```

An object can also be passed, which enables you to individually
configure each axis.

### [`mainAxis`](#mainaxis)

default: `0`

The axis that runs along the side of the floating element.
Represents the distance (gutter or margin) between the floating
element and the reference element.

```
offset({
  mainAxis: 10,
});
```

Here’s how it looks on the four sides:

top

Floating

bottom

Floating

left

Floating

right

Floating

### [`crossAxis`](#crossaxis)

default: `0`

The axis that runs along the alignment of the floating element.
Represents the skidding between the floating element and the
reference element.

```
offset({
  crossAxis: 20,
});
```

Here’s how it looks on the four sides:

top

Floating

bottom

Floating

left

Floating

right

Floating

### [`alignmentAxis`](#alignmentaxis)

default: `null`

The same axis as `crossAxis` but applies only to aligned
placements and inverts the `end` alignment. When set to
a number, it overrides the `crossAxis` value.

A positive number will move the floating element in the direction
of the opposite edge to the one that is aligned, while a negative
number the reverse.

```
offset({
  alignmentAxis: 20,
});
```

Here’s how it differentiates from `crossAxis`:

top-start   
 
**(crossAxis)**

Floating

top-end   
 
**(crossAxis)**

Floating

top-start   
 
**(alignmentAxis)**

Floating

top-end   
 
**(alignmentAxis)**

Floating

## [Creating custom placements](#creating-custom-placements)

While you can only choose 12 different placements as part of the
core library, you can use the `offset()` middleware to
create **any** placement you want.

For example, although the library doesn’t provide a placement for
centering on both axes, offset enables this via the function
option by allowing you to read the rects:

```
computePosition(referenceEl, floatingEl, {
  middleware: [
    // Assumes placement is 'bottom' (the default)
    offset(({rects}) => {
      return (
        -rects.reference.height / 2 - rects.floating.height / 2
      );
    }),
  ],
});
```

10px

Floating

In this case, the function option starts from the default bottom
placement, then using that starting point, returns an offset to
center the floating element on both axes.

A diagonal placement is also possible:

```
computePosition(referenceEl, floatingEl, {
  placement: 'top-start',
  middleware: [
    offset(({rects}) => ({
      alignmentAxis: -rects.floating.width,
    })),
  ],
});
```

Floating

This time, `'top-start'` was used as the starting point.

So, it’s straightforward to allow this:

```
computePosition(referenceEl, floatingEl, {
  placement: 'center',
});
```

With a wrapper, like this:

```
import {computePosition as base, offset} from '@floating-ui/dom';
 
const centerOffset = offset(({rects}) => {
  return -rects.reference.height / 2 - rects.floating.height / 2;
});
 
export function computePosition(
  referenceEl,
  floatingEl,
  options,
) {
  const isCentered = options.placement === 'center';
  const placement = isCentered ? 'bottom' : options.placement;
  const middleware = [
    isCentered && centerOffset,
    ...(options.middleware || []),
  ];
 
  return base(referenceEl, floatingEl, {
    ...options,
    placement,
    middleware,
  });
}
```