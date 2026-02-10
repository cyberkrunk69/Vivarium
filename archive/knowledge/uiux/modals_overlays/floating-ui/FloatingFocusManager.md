# FloatingFocusManager

Source: https://floating-ui.com/docs/FloatingFocusManager

---

# FloatingFocusManager

Provides flexible modal or non-modal focus management for a
floating element. Modal behavior is the default — focus is fully
trapped inside the floating element while it is rendered.

```
import {FloatingFocusManager} from '@floating-ui/react';
```

This is necessary to ensure that focus is properly managed for
keyboard interaction.

This component should only be rendered when the floating element
is open and directly wrap it.

```
function App() {
  const {context} = useFloating();
 
  return (
    <>
      {/* reference element */}
      {isOpen && (
        <FloatingFocusManager context={context}>
          {/* floating element */}
        </FloatingFocusManager>
      )}
    </>
  );
}
```

## [Props](#props)

```
interface FloatingFocusManagerProps {
  context: FloatingContext;
  disabled?: boolean;
  initialFocus?:
    | number
    | React.MutableRefObject<HTMLElement | null>;
  returnFocus?:
    | boolean
    | React.MutableRefObject<HTMLElement | null>;
  restoreFocus?: boolean;
  guards?: boolean;
  modal?: boolean;
  visuallyHiddenDismiss?: boolean | string;
  closeOnFocusOut?: boolean;
  outsideElementsInert?: boolean;
  getInsideElements?: () => Element[];
  order?: Array<'reference' | 'floating' | 'content'>;
}
```

### [`context`](#context)

Required

The `context` object returned from `useFloating()`
or
[`useFloatingRootContext`](/docs/useInteractions#external-reference).

```
<FloatingFocusManager context={context}>
  {/* floating element */}
</FloatingFocusManager>
```

### [`disabled`](#disabled)

default: `false`

Disables all focus management entirely. Useful to delay focus
management until after a transition completes or some other
conditional state.

```
<FloatingFocusManager context={context} disabled>
  {/* floating element */}
</FloatingFocusManager>
```

### [`initialFocus`](#initialfocus)

default: `0`

Which element to initially focus. Can be either a number
(tabbable index as specified by the `order`) or a ref.

```
<FloatingFocusManager
  context={context}
  initialFocus={elementRef}
>
  {/* floating element */}
</FloatingFocusManager>
```

#### [Negative number](#negative-number)

You can set this to a negative number to ignore the initial
focus. This is required to prevent conflicts if your floating
element has no tabbable content and is instead controlled by the
`useListNavigation()` Hook which has its own focus
management.

```
<FloatingFocusManager context={context} initialFocus={-1}>
  {/* floating element */}
</FloatingFocusManager>
```

If there is no list navigation, then `modal`
behavior’s focus trap will no longer work. To maintain the trap,
you can place the initial focus on the floating element:

```
const {context, refs} = useFloating();
 
return (
  <FloatingFocusManager
    context={context}
    initialFocus={refs.floating}
  >
    {/* floating element */}
  </FloatingFocusManager>
);
```

### [`returnFocus`](#returnfocus)

default: `true`

Determines if focus should be returned to the reference element
(or if that is not available, the previously focused element).
This prop is ignored if the floating element lost focus. It can
be also set to a ref to explicitly control the element to return
focus to.

```
<FloatingFocusManager context={context} returnFocus={false}>
  {/* floating element */}
</FloatingFocusManager>
```

### [`restoreFocus`](#restorefocus)

default: `false`

Determines if focus should be restored to the nearest tabbable
element if the currently focused element inside the floating
element was removed from the DOM (causing focus to be lost
otherwise).

```
<FloatingFocusManager context={context} restoreFocus={true}>
  {/* floating element */}
</FloatingFocusManager>
```

### [`guards`](#guards)

default: `true`

Determines if the focus guards are rendered. If not, focus can
escape into the address bar/console/browser UI, like in native
dialogs.

```
<FloatingFocusManager context={context} guards={false}>
  {/* floating element */}
</FloatingFocusManager>
```

### [`modal`](#modal)

default: `true`

Determines if focus is “modal”, meaning focus is fully trapped
inside the floating element and outside content cannot be
accessed. This includes screen reader virtual cursors.

```
<FloatingFocusManager context={context} modal={false}>
  {/* floating element */}
</FloatingFocusManager>
```

#### [Non-modal behavior](#non-modal-behavior)

The floating element should be rendered after the reference
element in the React tree. It can be portaled using
`<FloatingPortal>`. Other portal solutions are not supported
or accessible when using Floating UI’s focus manager.

#### [Modal behavior](#modal-behavior)

Ensure you have an explicit “close” button. This can be either
visible to all users, or visually-hidden so it is only available
to assistive tech (see
[`visuallyHiddenDismiss`](/docs/FloatingFocusManager#visuallyhiddendismiss)).
Touch-based screen readers often will not have an `esc` key
available to dismiss the element, so an explicit close button is
required, otherwise the user will be trapped in the floating
element if they don’t want to select anything (thus needing to
reload the page).

#### [Comboboxes](#comboboxes)

When the reference element has a `combobox`
`role` present, the focus manager behavior changes.

The listbox part (floating element) of a combobox (input +
listbox popup) can be portaled and accessible to touch screen
readers when using modal focus management, but DOM focus does not
become modal. Screen reader virtual cursors do become modal,
allowing a touch screen reader to immediately access the portaled
listbox items.

### [`visuallyHiddenDismiss`](#visuallyhiddendismiss)

default: `false`

If your focus management is modal and there is no explicit close
button available, you can use this prop to render a
visually-hidden dismiss button at the start and end of the
floating element. This allows touch-based screen readers to
escape the floating element due to lack of an `esc` key.

```
<FloatingFocusManager context={context} visuallyHiddenDismiss>
  {/* floating element */}
</FloatingFocusManager>
```

You can pass a string which will be announced by the screen
reader, e.g. for languages other than English. The default string
when using `true` is `Dismiss`.

```
<FloatingFocusManager
  context={context}
  visuallyHiddenDismiss="Dismiss popup"
>
  {/* floating element */}
</FloatingFocusManager>
```

### [`closeOnFocusOut`](#closeonfocusout)

default: `true`

Determines whether `focusout` event listeners that
control whether the floating element should be closed if the
focus moves outside of it are attached to the reference and
floating elements. This affects non-modal focus management.

```
<FloatingFocusManager context={context} closeOnFocusOut={false}>
  {/* floating element */}
</FloatingFocusManager>
```

### [`outsideElementsInert`](#outsideelementsinert)

default: `false`

Determines whether outside elements are `inert` when
`modal` is enabled. This enables pointer modality
without a backdrop.

```
<FloatingFocusManager context={context} outsideElementsInert>
  {/* floating element */}
</FloatingFocusManager>
```

### [`getInsideElements`](#getinsideelements)

Determines which elements are considered inside the floating
element when it’s rendered. Such elements will avoid being marked
with `aria-hidden` and `data-floating-ui-inert` attributes.

```
<FloatingFocusManager
  context={context}
  getInsideElements={() =>
    Array.from(document.querySelectorAll('.inside'))
  }
>
  {/* floating element */}
</FloatingFocusManager>
```

### [`order`](#order)

default: `['content']`

The order in which focus cycles.

```
<FloatingFocusManager
  context={context}
  // Initially focuses the floating element. Subsequent tabs
  // will cycle through the tabbable contents of the floating
  // element.
  order={['floating', 'content']}
  // Keeps focus on the reference element. Subsequent tabs
  // will cycle through the tabbable contents of the floating
  // element.
  order={['reference', 'content']}
>
  {/* floating element */}
</FloatingFocusManager>
```

## [Troubleshooting](#troubleshooting)

### [Page scrolls to top when opening the floating element](#page-scrolls-to-top-when-opening-the-floating-element)

This can happen if you’re placing the `autoFocus` prop
on an element inside the floating element. This is because the
floating element is initially rendered at the top-left of the
page, and the browser scrolls to it when it receives focus.

Instead, use the `initialFocus` prop on
`<FloatingFocusManager>` to focus the desired element, which
waits for the position to be ready first.

### [Usage with `<FloatingPortal>`](#usage-with-floatingportal)

Ensure the focus manager is rendered as a child (can be a nested
descendant) of `<FloatingPortal>`.

If you’re using non-modal focus management, you must use
`<FloatingPortal>` and not another portal solution. This is
because it tightly integrates with the focus manager to ensure
that focus is moved correctly when tabbing, including the
VoiceOver virtual cursor.