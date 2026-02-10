# FloatingPortal

Source: https://floating-ui.com/docs/FloatingPortal

---

# FloatingPortal

Portals the floating element into a given container element — by
default, outside of the app root and into the body.

```
import {FloatingPortal} from '@floating-ui/react';
```

This is necessary to ensure the floating element can appear
outside any potential parent containers that cause clipping (such
as `overflow: hidden`), while retaining its location in the React
tree.

```
function Tooltip() {
  if (isOpen) {
    return (
      <FloatingPortal>
        <div>Floating element</div>
      </FloatingPortal>
    );
  }
 
  return null;
}
```

Context is provided so that portals nested in one another are
appended to their respective parent.

## [Props](#props)

```
interface FloatingPortalProps {
  root?:
    | HTMLElement
    | null
    | React.MutableRefObject<HTMLElement | null>;
  id?: string;
  preserveTabOrder?: boolean;
}
```

### [`root`](#root)

Optionally specifies the root node the portal container will be
appended to.

```
// Element
<FloatingPortal root={rootNode} />
// MutableRefObject
<FloatingPortal root={rootNodeRef} />
```

### [`id`](#id)

Optionally selects the node with the id if it exists, or create
it and append it to the specified root (by default
`document.body`).

```
<FloatingPortal id="custom-root-id" />
```

### [`preserveTabOrder`](#preservetaborder)

default: `true`

When using non-modal focus management using
`<FloatingFocusManager />`, this will preserve the tab order
context based on the React tree instead of the DOM tree.

```
<FloatingPortal preserveTabOrder={false} />
```

## [`useFloatingPortalNode()`](#usefloatingportalnode)

Exposes the portal container node for custom use in other
components.

```
function App() {
  const portalNode = useFloatingPortalNode({
    // Accepts `id` and `root` props
  });
 
  if (portalNode) {
    return createPortal(<div />, portalNode);
  }
 
  return null;
}
```