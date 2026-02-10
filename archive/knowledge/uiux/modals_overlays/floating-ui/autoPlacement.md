# autoPlacement

Source: https://floating-ui.com/docs/autoPlacement

---

# autoPlacement

Chooses the placement that has the most space available
automatically.

*Visibility Optimizer*

```
import {autoPlacement} from '@floating-ui/dom';
```

This is useful when you don’t know which placement will be best
for the floating element, or don’t want to have to explicitly
specify it.

Scroll the container

Floating

## [Usage](#usage)

```
computePosition(referenceEl, floatingEl, {
  middleware: [autoPlacement()],
});
```

## [Options](#options)

These are the options you can pass to `autoPlacement()`.

```
interface AutoPlacementOptions extends DetectOverflowOptions {
  crossAxis?: boolean;
  alignment?: Alignment | null;
  autoAlignment?: boolean;
  allowedPlacements?: Array<Placement>;
}
```

### [`crossAxis`](#crossaxis)

default: `false`

Determines whether a “most space” strategy is also used for the
cross axis (which runs along the alignment of the floating
element). May be desirable when the `allowedPlacements`
are all on the same axis.

```
autoPlacement({
  crossAxis: true,
});
```

### [`alignment`](#alignment)

default: `undefined`

Without options, `autoPlacement()` will choose any of the
`Side` placements which fit best, i.e. `'top'`,
`'right'`, `'bottom'`, or `'left'`.

By specifying an alignment, it will choose those aligned
placements.

```
autoPlacement({
  // top-start, right-start, bottom-start, left-start
  alignment: 'start',
});
```

### [`autoAlignment`](#autoalignment)

default: `true`

When `alignment` is specified, this describes whether to
automatically choose placements with the opposite alignment if
they fit better.

```
autoPlacement({
  alignment: 'start',
  // Won't also choose 'end' alignments if those fit better
  autoAlignment: false,
});
```

### [`allowedPlacements`](#allowedplacements)

default: computed subset of `allPlacements`

Describes the placements which are allowed to be chosen.

```
autoPlacement({
  // 'right' and 'left' won't be chosen
  allowedPlacements: ['top', 'bottom'],
});
```

```
autoPlacement({
  // Only choose these placements
  allowedPlacements: ['top-start', 'bottom-end'],
});
```

### […detectOverflowOptions](#detectoverflowoptions)

All of [`detectOverflow`](/docs/detectOverflow#options)’s options
can be passed. For instance:

```
autoPlacement({
  padding: 5, // 0 by default
});
```

### [Deriving options from state](#deriving-options-from-state)

You can derive the options from the
[middleware lifecycle state](/docs/middleware#middlewarestate):

```
autoPlacement((state) => ({
  padding: state.rects.reference.width,
}));
```

## [Final placement](#final-placement)

The placement returned is always the final one.

```
computePosition(referenceEl, floatingEl, {
  middleware: [autoPlacement()],
}).then(({placement}) => {
  console.log(placement); // any side
});
```

## [Conflict with `flip()`](#conflict-with-flip)

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