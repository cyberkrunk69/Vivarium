# useInteractions

Source: https://floating-ui.com/docs/useInteractions

---

# useInteractions

A hook to merge or compose interaction event handlers together,
preserving memoization.

```
import {useInteractions} from '@floating-ui/react';
```

Interaction Hooks like `useHover()` and `useFocus()` do
two things: they create Effects inside themselves that work
independently, and also return event handlers intended to be
passed to the elements to add their functionality.

## [Usage](#usage)

`useInteractions()` accepts an array of the values returned
from interaction Hooks, merging their event handlers into prop
getters used for rendering:

```
import {
  useFloating,
  useHover,
  useFocus,
  useInteractions,
} from '@floating-ui/react';
 
function App() {
  const {context} = useFloating();
 
  const hover = useHover(context);
  const focus = useFocus(context);
 
  const {getReferenceProps, getFloatingProps} = useInteractions([
    hover,
    focus,
  ]);
}
```

## [External reference](#external-reference)

In your component API, the reference element may be external to
the component that `useFloating()` is called in (where the
positioning data is passed). In such a tree structure, the
interactions are shared between the reference element and
floating element in a “root” component higher than them — an
ancestor common to both.

An example would be:

```
<TooltipRoot> {/* useInteractions() called in this component */}
  <TooltipTrigger />
  <TooltipPopup /> {/* useFloating() called in this component */}
</TooltipRoot>
```

To share the interactions between the reference and floating
elements, you can use the `useFloatingRootContext()` Hook:

```
import {useFloatingRootContext} from '@floating-ui/react';
```

It returns a context object
that is accepted by all interaction Hooks, similar to the one
returned by `useFloating()` — only without the positioning
data.

Pass the open state and elements to the Hook:

```
function TooltipRoot() {
  const [isOpen, setIsOpen] = useState(false);
 
  const [anchor, setAnchor] = useState(null);
  const [tooltip, setTooltip] = useState(null);
 
  const context = useFloatingRootContext({
    open: isOpen,
    onOpenChange: setIsOpen,
    // Required: both elements must be passed externally.
    // Store them in state.
    elements: {
      reference: anchor,
      floating: tooltip,
    },
  });
 
  const click = useClick(context);
 
  const {getReferenceProps, getFloatingProps} = useInteractions([
    click,
  ]);
 
  return (
    <>
      <Anchor setAnchor={setAnchor} {...getReferenceProps()} />
      <Tooltip
        rootContext={context}
        setTooltip={setTooltip}
        {...getFloatingProps()}
      />;
    </>
  );
}
```

The root context must be available to `useFloating()` by
passing it as the `rootContext` option:

```
function Tooltip({rootContext, setTooltip, ...props}) {
  const {floatingStyles} = useFloating({
    rootContext,
  });
  return <div ref={setTooltip} {...props} />;
}
```

## [Return value](#return-value)

```
interface UseInteractionsReturn {
  getReferenceProps(
    userProps?: React.HTMLProps<Element>,
  ): Record<string, unknown>;
  getFloatingProps(
    userProps?: React.HTMLProps<HTMLElement>,
  ): Record<string, unknown>;
  getItemProps(
    userProps?: React.HTMLProps<HTMLElement>,
  ): Record<string, unknown>;
}
```

The Hook returns two core prop getters, one for the reference
element and one for the floating element. These prop getters
should be spread onto the elements:

```
<>
  <div ref={refs.setReference} {...getReferenceProps()} />
  <div
    ref={refs.setFloating}
    style={floatingStyles}
    {...getFloatingProps()}
  />
</>
```

All event handlers you pass in should be done so through the prop
getter, not the element itself:

```
<div
  ref={refs.setReference}
  {...getReferenceProps({
    onClick: () => console.log('clicked'),
    onFocus: () => console.log('focused'),
  })}
/>
```

This is because your handler may be either overwritten or
overwrite one of the Hooks’ handlers. More event handlers may
also be added in future versions.

## [`getItemProps`](#getitemprops)

A third prop getter is returned for item elements when dealing
with a list inside the floating element, which is not required
for all types of floating elements. See
[`useRole`](/docs/useRole#role) for more information on this prop
getter for listbox (e.g. select or combobox) or menu roles.

```
const {
  getReferenceProps, 
  getFloatingProps, 
  getItemProps
} = useInteractions([]);
```