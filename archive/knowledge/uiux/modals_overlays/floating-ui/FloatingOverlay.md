# FloatingOverlay

Source: https://floating-ui.com/docs/FloatingOverlay

---

# FloatingOverlay

Provides base styling for a fixed overlay element.

```
import {FloatingOverlay} from '@floating-ui/react';
```

This is useful to dim content or block pointer events behind a
floating element, in addition to locking the body scroll.

## [Usage](#usage)

It renders a `<div>` with base styling.

```
function App() {
  return (
    <>
      <FloatingOverlay />
      <div>Floating element</div>
    </>
  );
}
```

## [Props](#props)

```
interface FloatingOverlayProps {
  lockScroll?: boolean;
}
```

### [`lockScroll`](#lockscroll)

Whether the `<body>` is prevented from scrolling while the
overlay is rendered. Uses a robust technique that works on iOS
and handles horizontal scrolling.

```
<FloatingOverlay lockScroll>
  {/* floating element */}
</FloatingOverlay>
```

## [Troubleshooting](#troubleshooting)

### [Sibling Overlay](#sibling-overlay)

When using anchor positioning and the overlay in scrollable
contexts, prefer making the overlay a sibling of the floating
element rather than a parent container.

This will ensure the floating element does not get contained by
the overlay, allowing it to be positioned out of its bounds,
preventing scroll issues. It also allows the overlay to be
independently animated.

```
<>
  <FloatingOverlay />
  <div ref={refs.setFloating} />
</>
```