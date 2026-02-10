# useFloating

Source: https://floating-ui.com/docs/useFloating

---

# useFloating

The main Hook of the library that acts as a controller for all
other Hooks and components.

## [Usage](#usage)

Call the Hook inside a component.

```
function App() {
  const {refs, floatingStyles} = useFloating();
  return (
    <>
      <div ref={refs.setReference} />
      <div ref={refs.setFloating} style={floatingStyles} />
    </>
  );
}
```

## [Options](#options)

The Hook accepts an object of options to configure its behavior.

```
useFloating({
  // options
});
```

### [`placement`](#placement)

default: `'bottom'`

The placement of the floating element relative to the reference
element.

```
useFloating({
  placement: 'left',
});
```

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

The `-start` and `-end` alignments are
[logical](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties)
and will adapt to the writing direction (e.g. RTL) as expected.

### [`strategy`](#strategy)

default: `'absolute'`

This is the type of CSS position property to use. Two strings are
available:

```
type Strategy = 'absolute' | 'fixed';
```

```
useFloating({
  strategy: 'fixed',
});
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

### [`transform`](#transform)

default: `true`

Whether to use CSS transforms to position the floating element
instead of layout (`top` and `left` CSS properties).

```
useFloating({
  transform: false,
});
```

CSS transforms are more performant, but can cause conflicts with
transform animations. In that case, you can make the positioned
floating element a wrapper to avoid the conflict:

```
<div ref={refs.setFloating} style={floatingStyles}>
  <div style={transitionStyles}>Content</div>
</div>
```

### [`middleware`](#middleware)

default: `[]`

An array of middleware objects that change the positioning of the
floating element.

```
useFloating({
  middleware: [
    // ...
  ],
});
```

When you want granular control over how the floating element is
positioned, middleware are used. They read the current
coordinates, optionally alter them, and/or provide data for
rendering. They compose and work together to produce the final
coordinates which are in the `floatingStyles` object.

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

#### [Option reactivity](#option-reactivity)

When using React state and middleware, stateful values inside
*functions* aren’t fresh or reactive.

```
const [value, setValue] = useState(0);
 
offset(value); // reactive and fresh
offset(() => value); // NOT reactive or fresh
```

Specifying the dependencies as a second argument of any
middleware function will keep it reactive:

```
offset(() => value, [value]);
```

This goes for any function option, including `size()`’s
`apply` function.

### [`elements`](#elements)

default: `undefined`

An object of elements passed to the Hook, which is useful for
externally passing them, as an alternative to the `refs`
object setters.

The elements must be held in state (not plain refs) to ensure
that they are reactive.

```
const [reference, setReference] = useState(null);
 
const {refs} = useFloating({
  elements: {
    reference,
  },
});
 
return (
  <>
    <div ref={setReference} />
    <div ref={refs.setFloating} />
  </>
);
```

You can also do the inverse of the above, or pass both
externally.

### [`whileElementsMounted`](#whileelementsmounted)

default: `undefined`

A function that is called when the reference and floating
elements are mounted, and returns a cleanup function called when
they are unmounted.

```
useFloating({
  whileElementsMounted: (reference, floating, update) => {
    // ...
    return () => {
      // ...
    };
  },
});
```

This allows you to pass [`autoUpdate`](/docs/autoUpdate) whose
signature matches the option, to ensure the floating element
remains anchored to the reference element:

```
import {autoUpdate} from '@floating-ui/react';
 
useFloating({
  whileElementsMounted: autoUpdate,
});
```

### [`open`](#open)

default: `false`

Whether the floating element is open or not, which allows you to
determine if the floating element has been positioned yet.

```
const [isOpen, setIsOpen] = useState(false);
 
const {isPositioned} = useFloating({
  open: isOpen,
});
 
// Once `isOpen` flips to `true`, `isPositioned` will switch to `true`
// asynchronously. We can use an Effect to determine when it has
// been positioned.
useEffect(() => {
  if (isPositioned) {
    // ...
  }
}, [isPositioned]);
```

## [Return value](#return-value)

The Hook returns the following type:

```
interface UseFloatingReturn {
  context: FloatingContext;
  placement: Placement;
  strategy: Strategy;
  x: number;
  y: number;
  middlewareData: MiddlewareData;
  isPositioned: boolean;
  update(): void;
  floatingStyles: React.CSSProperties;
  refs: {
    reference: React.MutableRefObject<ReferenceElement | null>;
    floating: React.MutableRefObject<HTMLElement | null>;
    domReference: React.MutableRefObject<Element | null>;
    setReference(node: RT | null): void;
    setFloating(node: HTMLElement | null): void;
    setPositionReference(node: ReferenceElement): void;
  };
  elements: {
    reference: RT | null;
    floating: HTMLElement | null;
  };
}
```

### [`placement`](#placement-1)

The **final** placement of the floating element relative to the
reference element. Unlike the one passed in the options, this one
can be mutated by middleware like `flip()`. This is
necessary to determine the actual side of the floating element
for styling.

```
const {placement} = useFloating();
```

### [`strategy`](#strategy-1)

The positioning strategy of the floating element.

```
const {strategy} = useFloating();
```

### [`x`](#x)

The final x-coordinate of the floating element. This can be used
as an alternative to `floatingStyles` to manually position the
floating element with custom CSS.

```
const {x} = useFloating();
```

### [`y`](#y)

The final y-coordinate of the floating element. This can be used
as an alternative to `floatingStyles` to manually position the
floating element with custom CSS.

```
const {y} = useFloating();
```

### [`middlewareData`](#middlewaredata)

The data provided by any middleware used.

```
const {middlewareData} = useFloating();
```

### [`isPositioned`](#ispositioned)

Whether the floating element has been positioned yet when used
inside an Effect (not during render). Requires the `open`
option to be passed.

```
const {isPositioned} = useFloating();
```

### [`update`](#update)

A function that updates the floating element’s position manually.

```
const {update} = useFloating();
```

### [`floatingStyles`](#floatingstyles)

The styles that should be applied to the floating element.

```
const {floatingStyles} = useFloating();
```

### [`refs`](#refs)

The refs that should be applied to the reference and floating
elements.

```
const {refs} = useFloating();
```

#### [`reference`](#reference)

A ref for the reference element. You can access this inside an
event handler or in an Effect.

```
const {refs} = useFloating();
useEffect(() => {
  console.log(refs.reference.current);
}, [refs]);
```

#### [`floating`](#floating)

A ref for the floating element. You can access this inside an
event handler.

For usage in Effects, prefer using `elements.floating`,
since it’s not guaranteed the floating element will be available
on the first pass.

```
const {refs} = useFloating();
// Inside an event handler:
console.log(refs.floating.current);
```

#### [`setReference`](#setreference)

A function that sets the reference element.

```
const {refs} = useFloating();
return <div ref={refs.setReference} />;
```

#### [`setFloating`](#setfloating)

A function that sets the floating element.

```
const {refs} = useFloating();
return <div ref={refs.setFloating} />;
```

### [`elements`](#elements-1)

The elements as set by the refs, useful for access during
rendering or when needing to reactively check if the element
exists.

```
const {elements} = useFloating();
```

#### [`reference`](#reference-1)

The reference element. May be virtual.

```
const {elements} = useFloating();
console.log(elements.reference);
```

#### [`floating`](#floating-1)

The floating element. Enables you to reactively check if the
floating element exists inside Effects, notable when using
`<FloatingPortal>`, as it won’t be available on the first
pass.

```
const {elements} = useFloating();
React.useEffect(() => {
  if (!elements.floating) return;
  // ...
}, [elements.floating]);
```