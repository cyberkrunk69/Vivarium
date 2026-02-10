# useDismiss

Source: https://floating-ui.com/docs/useDismiss

---

# useDismiss

Closes the floating element when a dismissal is requested — by
default, when the user presses the `escape` key or outside of the
floating element with their pointer.

```
import {useDismiss} from '@floating-ui/react';
```

This is useful to ensure the floating element is closed when the
user is finished interacting with it, including keyboard support.

## [Usage](#usage)

This Hook returns event handler props.

To use it, pass it the `context` object returned from
`useFloating()` or
[`useFloatingRootContext`](/docs/useInteractions#external-reference),
and then feed its result into the `useInteractions()` array.
The returned prop getters are then spread onto the elements for
rendering.

```
function App() {
  const [isOpen, setIsOpen] = useState(false);
 
  const {refs, floatingStyles, context} = useFloating({
    open: isOpen,
    onOpenChange: setIsOpen,
  });
 
  const dismiss = useDismiss(context);
 
  const {getReferenceProps, getFloatingProps} = useInteractions([
    dismiss,
  ]);
 
  return (
    <>
      <div ref={refs.setReference} {...getReferenceProps()}>
        Reference element
      </div>
      {isOpen && (
        <div
          ref={refs.setFloating}
          style={floatingStyles}
          {...getFloatingProps()}
        >
          Floating element
        </div>
      )}
    </>
  );
}
```

## [Props](#props)

```
interface UseDismissProps {
  enabled?: boolean;
  escapeKey?: boolean;
  referencePress?: boolean;
  referencePressEvent?: 'pointerdown' | 'mousedown' | 'click';
  outsidePress?: boolean | ((event: MouseEvent) => boolean);
  outsidePressEvent?: 'pointerdown' | 'mousedown' | 'click';
  ancestorScroll?: boolean;
  bubbles?:
    | boolean
    | {escapeKey?: boolean; outsidePress?: boolean};
  capture?:
    | boolean
    | {escapeKey?: boolean; outsidePress?: boolean};
}
```

### [`enabled`](#enabled)

default: `true`

Conditionally enable/disable the Hook.

```
useDismiss(context, {
  enabled: false,
});
```

### [`escapeKey`](#escapekey)

default: `true`

Whether to dismiss the floating element upon pressing the `esc`
key.

```
useDismiss(context, {
  escapeKey: false,
});
```

### [`referencePress`](#referencepress)

default: `false`

Whether to dismiss the floating element upon pressing the
reference element.

```
useDismiss(context, {
  referencePress: true,
});
```

You likely want to ensure the `move` option in the
`useHover()` hook has been disabled when this is in use.

### [`referencePressEvent`](#referencepressevent)

default: `'pointerdown'`

The type of event to use to determine a “press”.

```
useDismiss(context, {
  // Eager on both mouse + touch input.
  referencePressEvent: 'pointerdown',
  // Eager on mouse input; lazy on touch input.
  referencePressEvent: 'mousedown',
  // Lazy on both mouse + touch input.
  referencePressEvent: 'click',
});
```

### [`outsidePress`](#outsidepress)

default: `true`

Whether to dismiss the floating element upon pressing outside of
both the floating and reference elements.

```
useDismiss(context, {
  outsidePress: false,
});
```

If you have another element, like a toast, that is rendered
outside the floating element’s React tree and don’t want the
floating element to close when pressing it, you can guard the
check like so:

```
useDismiss(context, {
  // Same as `true`, but with a custom guard check.
  outsidePress: (event) => !event.target.closest('.toast'),
});
```

```
function App() {
  // The toast is not inside the Dialog's React tree, so we
  // need to add a guard to consider it a child of the Dialog
  // to prevent the Dialog's outside press from closing it.
  return (
    <>
      <Dialog />
      <Toast className="toast" />
    </>
  );
}
```

### [`outsidePressEvent`](#outsidepressevent)

default: `'pointerdown'`

The type of event to use to determine a “press”.

```
useDismiss(context, {
  // Eager on both mouse + touch input.
  outsidePressEvent: 'pointerdown',
  // Eager on mouse input; lazy on touch input.
  outsidePressEvent: 'mousedown',
  // Lazy on both mouse + touch input.
  outsidePressEvent: 'click',
});
```

### [`ancestorScroll`](#ancestorscroll)

default: `false`

Whether to dismiss the floating element upon scrolling an
overflow ancestor.

```
useDismiss(context, {
  ancestorScroll: true,
});
```

### [`bubbles`](#bubbles)

default: `undefined`

Determines whether event listeners bubble upwards through a tree
of floating elements.

- `escapeKey` determines whether pressing the `esc` key
  bubbles, causing ancestor floating elements to dismiss as well.
  For instance, if you’re dismissing a tooltip inside a dialog
  using the `esc` key, you likely don’t want the dialog to
  dismiss as well until a second key press, which is the default
  behavior.
- `outsidePress` determines whether pressing outside of a
  child floating element bubbles, causing ancestor floating
  elements to dismiss as well. Setting this to `false`
  requires a [`FloatingTree`](/docs/FloatingTree) to be set up.

```
useDismiss(context, {
  // Configure bubbling for all relevant events:
  bubbles: false,
  // Or, individually configure by event:
  bubbles: {
    escapeKey: true, // false by default
    outsidePress: false, // true by default
  },
});
```

### [`capture`](#capture)

default: `undefined`

Determines whether to use capture phase event listeners.

```
useDismiss(context, {
  // Configure capturing for all relevant events:
  capture: true,
  // Or, individually configure by event:
  capture: {
    escapeKey: true, // false by default
    outsidePress: false, // true by default
  },
});
```

## [Reacting to dismissal](#reacting-to-dismissal)

To react to the dismissal event, you can check for the
`reason` string in the `onOpenChange`
callback:

```
useFloating({
  open: isOpen,
  onOpenChange(nextOpen, event, reason) {
    setIsOpen(nextOpen);
 
    // Other ones include 'reference-press' and 'ancestor-scroll'
    // if enabled.
    if (reason === 'escape-key' || reason === 'outside-press') {
      console.log('Dismissed');
    }
  },
});
```

## [Troubleshooting](#troubleshooting)

### [Does not close when clicking in an iframe](#does-not-close-when-clicking-in-an-iframe)

You can use the
[`FloatingOverlay` component](/docs/FloatingOverlay) which will
“cover” iframes to ensure clicks are captured in the same
document as the floating element, as the click occurs on the
overlay backdrop. This guarantees “outside press” detection will
work.