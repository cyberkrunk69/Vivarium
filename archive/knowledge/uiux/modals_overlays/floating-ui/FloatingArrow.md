# FloatingArrow

Source: https://floating-ui.com/docs/FloatingArrow

---

# FloatingArrow

Renders a customizable `<svg>` pointing arrow triangle
inside the floating element that gets automatically positioned.

```
import {FloatingArrow} from '@floating-ui/react';
```

Floating

Floating

Floating

Floating

## [Usage](#usage)

- Create an arrowRef and
  pass it to the [arrow middleware](/docs/arrow)’s
  `element` option and the `<FloatingArrow />`
  component. This lets the arrow be measured for positioning.
- Pass the context to the
  `<FloatingArrow />` component. This lets the component
  read the positioning data.

```
import {FloatingArrow, arrow} from '@floating-ui/react';
 
function App() {
  const arrowRef = useRef(null);
  const {refs, floatingStyles, context} = useFloating({
    middleware: [
      arrow({
        element: arrowRef,
      }),
    ],
  });
 
  return (
    <>
      <div ref={refs.setReference} />
      <div ref={refs.setFloating} style={floatingStyles}>
        <FloatingArrow ref={arrowRef} context={context} />
      </div>
    </>
  );
}
```

The arrow will, by default, overlap the reference element. The
`height` of the arrow will offset it by the desired
amount.

```
import {offset} from '@floating-ui/react';
 
const ARROW_HEIGHT = 7;
const GAP = 2;
 
useFloating({
  middleware: [offset(ARROW_HEIGHT + GAP)],
});
```

This does not take into account tip rounding or strokes.

## [Props](#props)

The arrow accepts all the props of an `<svg>` element, plus
some additional props:

```
interface Props extends React.SVGAttributes<SVGSVGElement> {
  context: FloatingContext;
  width?: number;
  height?: number;
  tipRadius?: number;
  staticOffset?: number | string | null;
 
  // Inherited SVG props that are intercepted and passed
  // to the <path>s
  d?: string;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
}
```

### [`ref`](#ref)

Required

```
<FloatingArrow ref={arrowRef} />
```

### [`context`](#context)

Required

The `context` object returned from `useFloating()`.

```
const {context} = useFloating();
<FloatingArrow context={context} />;
```

### [`width`](#width)

default: `14`

The width of the arrow.

```
<FloatingArrow ref={arrowRef} context={context} width={10} />
```

### [`height`](#height)

default: `7`

The height of the arrow.

```
<FloatingArrow ref={arrowRef} context={context} height={10} />
```

### [`tipRadius`](#tipradius)

default: `0` (sharp)

The radius (rounding) of the arrow tip.

```
<FloatingArrow ref={arrowRef} context={context} tipRadius={2} />
```

### [`staticOffset`](#staticoffset)

default: `undefined` (use dynamic position)

A static offset override of the arrow from the floating element
edge. Often desirable if the floating element is smaller than the
reference element along the relevant axis and has an edge
alignment (`'start'`/`'end'`). This is ignored if the
shift() middleware caused the floating element to shift.

```
<FloatingArrow
  ref={arrowRef}
  context={context}
  staticOffset={isEdgeAlignedAndSmaller ? '15%' : null}
/>
```

### [`d`](#d)

default: `undefined` (use dynamic path)

A custom path for the arrow. Useful if you want fancy rounding.
The path should be inside a square SVG and placed at the bottom
of it. The path is designed for the `'bottom'` placement,
which will be rotated for other placements.

```
<FloatingArrow
  ref={arrowRef}
  context={context}
  width={20}
  height={20}
  d="M0 20C0 20 2.06906 19.9829 5.91817 15.4092C7.49986 13.5236 8.97939 12.3809 10.0002 12.3809C11.0202 12.3809 12.481 13.6451 14.0814 15.5472C17.952 20.1437 20 20 20 20H0Z"
/>
```

### [`fill`](#fill)

default: `"black"` (browser default)

The color of the arrow.

```
<FloatingArrow ref={arrowRef} context={context} fill="red" />
```

### [`stroke`](#stroke)

default: `"none"`

The stroke (border) color of the arrow.

```
<FloatingArrow ref={arrowRef} context={context} stroke="red" />
```

### [`strokeWidth`](#strokewidth)

default: `0`

The stroke (border) width of the arrow. This must match (or be
less than) the floating element’s border width.

```
<FloatingArrow
  ref={arrowRef}
  context={context}
  strokeWidth={2}
/>
```

## [Tailwind and utility CSS styling](#tailwind-and-utility-css-styling)

- `fill-*` sets the arrow’s fill color.
- `[&>path:first-of-type]` targets the “stroke” path.
- `[&>path:last-of-type]` targets the “fill” path’s
  extra stroke, to reduce gaps.

`strokeWidth` should still be manually specified as a
prop.

```
<FloatingArrow
  ref={arrowRef}
  context={context}
  className="
    fill-white 
    [&>path:first-of-type]:stroke-pink-500
    [&>path:last-of-type]:stroke-white
  "
/>
```

## [Scale transforms](#scale-transforms)

When animating the floating element’s scale, it looks best if the
floating element’s `transform-origin` is at the tip of the arrow.
The `arrow` middleware provides data to achieve this.

[View on CodeSandbox](https://codesandbox.io/s/floating-ui-react-scale-transform-origin-qv0t1c?file=/src/App.tsx)

## [Troubleshooting](#troubleshooting)

### [Stroke is not visible](#stroke-is-not-visible)

Ensure you’ve specified at least a `strokeWidth` of
`1`.

### [A gap is present](#a-gap-is-present)

- Styling the top-level `<svg>` using native CSS properties
  like `fill` and `stroke` directly won’t work correctly. This
  can happen if you’re styling using `styled(FloatingArrow)`
  for example. Instead, use the `fill` and
  `stroke` props, or target the child path elements as
  shown in
  [Tailwind and utility CSS styling](/docs/FloatingArrow#tailwind-and-utility-css-styling).
- If a border is applied to an inner element of the floating
  element, make sure arrow is inside the inner element and that
  the inner element has `position: relative` CSS. This
  ensures the arrow will align with the border correctly.
- Ensure the `strokeWidth` of the arrow is the same as
  the floating element’s border width.
- The gap may be related to zoom levels in some browsers or the
  OS. To support transparency and prevent overlapping of colors
  of the floating and arrow element, this problem cannot be
  avoided. If your floating element and arrow are not partially
  transparent and are instead solid colors, you can use the
  following workaround:

```
<FloatingArrow style={{ transform: 'translateY(-1px)' }}>
```

### [Arrow does not avoid rounded corners](#arrow-does-not-avoid-rounded-corners)

The arrow doesn’t automatically avoid rounded corners of the
floating element when it’s shifted. To ensure it doesn’t overflow
the corners, you can use the `padding` prop in the
`arrow()` middleware when calling `useFloating()` to
account for this.