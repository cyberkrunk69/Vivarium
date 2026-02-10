# Reorder â React drag-to-reorder animation | Motion

Source: https://www.framer.com/motion/reorder/

---

The `Reorder` components can be used to create drag-to-reorder lists, like reorderable tabs or todo items.

```
const [items, setItems] = useState([0, 1, 2, 3])

return (
  <Reorder.Group axis="y" values={items} onReorder={setItems}>
    {items.map((item) => (
      <Reorder.Item key={item} value={item}>
        {item}
      </Reorder.Item>
    ))}
  </Reorder.Group>
)
```

`Reorder` is for simple drag-to-reorder implementations. It's exceptionally lightweight ontop of the base `motion` component but lacks some features like multirow, dragging between columns, or dragging within scrollable containers. For advanced use-cases we recommend something like [DnD Kit](https://docs.dndkit.com/).

## [Usage](#usage)

Every reorderable list is wrapped in the `Reorder.Group` component.

```
import { Reorder } from "motion/react"

function List() {
  return (
    <Reorder.Group>
    
    </Reorder.Group>
  )
}
```

By default, this is rendered as a `<ul>`, but this can be changed with the `as` prop.

```
<Reorder.Group as="ol">
```

`Reorder.Group` must be passed the array of values in your reorderable list via the `values` prop.

Additionally, a `onReorder` event will fire with the latest calculated order. For items to reorder, this must update the `values` state.

```
import { Reorder } from "framer-motion"

function List() {
  const [items, setItems] = useState([0, 1, 2, 3])

  return (
    <Reorder.Group values={items} onReorder={setItems}>
    
    </Reorder.Group>
  )
}
```

To render each reorderable item, use `Reorder.Item`, passing it the value it represents via the `value` prop.

```
import { Reorder } from "framer-motion"

function List() {
  const [items, setItems] = useState([0, 1, 2, 3])

  return (
    <Reorder.Group values={items} onReorder={setItems}>
      {items.map(item => (
        <Reorder.Item key={item} value={item}>
          {item}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  )
}
```

Now, when items are dragged and reordered, `onReorder` will fire with a new order.

### [Layout animations](#layout-animations)

`Reorder.Item` components are already configured to perform [layout animations](./react-layout-animations), so if new items are added or removed to the reorderable list, surrounding items will animate to their new position automatically.

### [Exit animations](#exit-animations)

`AnimatePresence` can be used as normal to animate items as they enter/leave the React tree.

```
<AnimatePresence>
  {items.map(item => (
    <Reorder.Item
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      key={item}
    />  
  ))}
</AnimatePresence>
```

### [Drag triggers](#drag-triggers)

By default, all of a `Reorder.Item` will be draggable. `useDragControls` can be used to define a different component to act as a drag trigger.

```
import { Reorder, useDragControls } from "framer-motion"

function Item({ value }) {
  const controls = useDragControls()
  
  return (
    <Reorder.Item
      value={value}
      dragListener={false}
      dragControls={controls}
    >
      <div
        className="reorder-handle"
        onPointerDown={(e) => controls.start(e)}
      />
    </Reorder.Item>
  )
}
```

### [Auto-scroll lists](#auto-scroll-lists)

If a `Reorder.Group` is within a scrollable container, the container will automatically scroll when a user drags an item towards the top and bottom of the list.

The closer to the edge of the container, the faster the scroll.

### [z-index](#z-index)

`Reorder.Item` will automatically set a `z-index` style on the currently dragged item so it appears above the surrounding items.

However, `z-index` only affects items with `position !== "static"`. So to enable this effect ensure the position of the `Reorder.Item` is set to `relative` or `absolute`.

## [API](#api)

### [`Reorder.Group`](#reorder.group)

#### [`as`](#as)

**Default**: `"ul"`

The underlying element for `Reorder.Group` to render as.

```
<Reorder.Group as="div"></Reorder.Group>
```

#### [`axis`](#axis)

**Default**: `"y"`

The direction of reorder detection.

By default, all `Reorder.Item` components will visibly move only on this axis. To allow visual motion (but **not** reordering) on both axes, pass the `drag` prop to child `Reorder.Item` components.

#### [`values`](#values)

The values array that will be reordered. Each item in this list must match a `value` passed to each `Reorder.Item`.

#### [`onReorder`](#onreorder)

A callback that will fire when items are detected to have reordered. The provided `newOrder` should be passed to a `values` state update function.

```
const [items, setItems] = useState([0, 1, 2, 3])

return (
  <Reorder.Group values={items} onReorder={setItems}>
```

### [`Reorder.Item`](#reorder.item)

`Reorder.Item` components accept all `motion` [component props](./react-motion-component) in addition to the following:

#### [`as`](#as-1)

**Default:** `"li"`

The element for `Reorder.Item` to render as.

#### [`value`](#value)

When `onReorder` is called, this is the value that will be passed through in the newly ordered array.

The `Reorder` components can be used to create drag-to-reorder lists, like reorderable tabs or todo items.

```
const [items, setItems] = useState([0, 1, 2, 3])

return (
  <Reorder.Group axis="y" values={items} onReorder={setItems}>
    {items.map((item) => (
      <Reorder.Item key={item} value={item}>
        {item}
      </Reorder.Item>
    ))}
  </Reorder.Group>
)
```

`Reorder` is for simple drag-to-reorder implementations. It's exceptionally lightweight ontop of the base `motion` component but lacks some features like multirow, dragging between columns, or dragging within scrollable containers. For advanced use-cases we recommend something like [DnD Kit](https://docs.dndkit.com/).

## [Usage](#usage)

Every reorderable list is wrapped in the `Reorder.Group` component.

```
import { Reorder } from "motion/react"

function List() {
  return (
    <Reorder.Group>
    
    </Reorder.Group>
  )
}
```

By default, this is rendered as a `<ul>`, but this can be changed with the `as` prop.

```
<Reorder.Group as="ol">
```

`Reorder.Group` must be passed the array of values in your reorderable list via the `values` prop.

Additionally, a `onReorder` event will fire with the latest calculated order. For items to reorder, this must update the `values` state.

```
import { Reorder } from "framer-motion"

function List() {
  const [items, setItems] = useState([0, 1, 2, 3])

  return (
    <Reorder.Group values={items} onReorder={setItems}>
    
    </Reorder.Group>
  )
}
```

To render each reorderable item, use `Reorder.Item`, passing it the value it represents via the `value` prop.

```
import { Reorder } from "framer-motion"

function List() {
  const [items, setItems] = useState([0, 1, 2, 3])

  return (
    <Reorder.Group values={items} onReorder={setItems}>
      {items.map(item => (
        <Reorder.Item key={item} value={item}>
          {item}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  )
}
```

Now, when items are dragged and reordered, `onReorder` will fire with a new order.

### [Layout animations](#layout-animations)

`Reorder.Item` components are already configured to perform [layout animations](./react-layout-animations), so if new items are added or removed to the reorderable list, surrounding items will animate to their new position automatically.

### [Exit animations](#exit-animations)

`AnimatePresence` can be used as normal to animate items as they enter/leave the React tree.

```
<AnimatePresence>
  {items.map(item => (
    <Reorder.Item
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      key={item}
    />  
  ))}
</AnimatePresence>
```

### [Drag triggers](#drag-triggers)

By default, all of a `Reorder.Item` will be draggable. `useDragControls` can be used to define a different component to act as a drag trigger.

```
import { Reorder, useDragControls } from "framer-motion"

function Item({ value }) {
  const controls = useDragControls()
  
  return (
    <Reorder.Item
      value={value}
      dragListener={false}
      dragControls={controls}
    >
      <div
        className="reorder-handle"
        onPointerDown={(e) => controls.start(e)}
      />
    </Reorder.Item>
  )
}
```

### [Auto-scroll lists](#auto-scroll-lists)

If a `Reorder.Group` is within a scrollable container, the container will automatically scroll when a user drags an item towards the top and bottom of the list.

The closer to the edge of the container, the faster the scroll.

### [z-index](#z-index)

`Reorder.Item` will automatically set a `z-index` style on the currently dragged item so it appears above the surrounding items.

However, `z-index` only affects items with `position !== "static"`. So to enable this effect ensure the position of the `Reorder.Item` is set to `relative` or `absolute`.

## [API](#api)

### [`Reorder.Group`](#reorder.group)

#### [`as`](#as)

**Default**: `"ul"`

The underlying element for `Reorder.Group` to render as.

```
<Reorder.Group as="div"></Reorder.Group>
```

#### [`axis`](#axis)

**Default**: `"y"`

The direction of reorder detection.

By default, all `Reorder.Item` components will visibly move only on this axis. To allow visual motion (but **not** reordering) on both axes, pass the `drag` prop to child `Reorder.Item` components.

#### [`values`](#values)

The values array that will be reordered. Each item in this list must match a `value` passed to each `Reorder.Item`.

#### [`onReorder`](#onreorder)

A callback that will fire when items are detected to have reordered. The provided `newOrder` should be passed to a `values` state update function.

```
const [items, setItems] = useState([0, 1, 2, 3])

return (
  <Reorder.Group values={items} onReorder={setItems}>
```

### [`Reorder.Item`](#reorder.item)

`Reorder.Item` components accept all `motion` [component props](./react-motion-component) in addition to the following:

#### [`as`](#as-1)

**Default:** `"li"`

The element for `Reorder.Item` to render as.

#### [`value`](#value)

When `onReorder` is called, this is the value that will be passed through in the newly ordered array.

The `Reorder` components can be used to create drag-to-reorder lists, like reorderable tabs or todo items.

```
const [items, setItems] = useState([0, 1, 2, 3])

return (
  <Reorder.Group axis="y" values={items} onReorder={setItems}>
    {items.map((item) => (
      <Reorder.Item key={item} value={item}>
        {item}
      </Reorder.Item>
    ))}
  </Reorder.Group>
)
```

`Reorder` is for simple drag-to-reorder implementations. It's exceptionally lightweight ontop of the base `motion` component but lacks some features like multirow, dragging between columns, or dragging within scrollable containers. For advanced use-cases we recommend something like [DnD Kit](https://docs.dndkit.com/).

## [Usage](#usage)

Every reorderable list is wrapped in the `Reorder.Group` component.

```
import { Reorder } from "motion/react"

function List() {
  return (
    <Reorder.Group>
    
    </Reorder.Group>
  )
}
```

By default, this is rendered as a `<ul>`, but this can be changed with the `as` prop.

```
<Reorder.Group as="ol">
```

`Reorder.Group` must be passed the array of values in your reorderable list via the `values` prop.

Additionally, a `onReorder` event will fire with the latest calculated order. For items to reorder, this must update the `values` state.

```
import { Reorder } from "framer-motion"

function List() {
  const [items, setItems] = useState([0, 1, 2, 3])

  return (
    <Reorder.Group values={items} onReorder={setItems}>
    
    </Reorder.Group>
  )
}
```

To render each reorderable item, use `Reorder.Item`, passing it the value it represents via the `value` prop.

```
import { Reorder } from "framer-motion"

function List() {
  const [items, setItems] = useState([0, 1, 2, 3])

  return (
    <Reorder.Group values={items} onReorder={setItems}>
      {items.map(item => (
        <Reorder.Item key={item} value={item}>
          {item}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  )
}
```

Now, when items are dragged and reordered, `onReorder` will fire with a new order.

### [Layout animations](#layout-animations)

`Reorder.Item` components are already configured to perform [layout animations](./react-layout-animations), so if new items are added or removed to the reorderable list, surrounding items will animate to their new position automatically.

### [Exit animations](#exit-animations)

`AnimatePresence` can be used as normal to animate items as they enter/leave the React tree.

```
<AnimatePresence>
  {items.map(item => (
    <Reorder.Item
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      key={item}
    />  
  ))}
</AnimatePresence>
```

### [Drag triggers](#drag-triggers)

By default, all of a `Reorder.Item` will be draggable. `useDragControls` can be used to define a different component to act as a drag trigger.

```
import { Reorder, useDragControls } from "framer-motion"

function Item({ value }) {
  const controls = useDragControls()
  
  return (
    <Reorder.Item
      value={value}
      dragListener={false}
      dragControls={controls}
    >
      <div
        className="reorder-handle"
        onPointerDown={(e) => controls.start(e)}
      />
    </Reorder.Item>
  )
}
```

### [Auto-scroll lists](#auto-scroll-lists)

If a `Reorder.Group` is within a scrollable container, the container will automatically scroll when a user drags an item towards the top and bottom of the list.

The closer to the edge of the container, the faster the scroll.

### [z-index](#z-index)

`Reorder.Item` will automatically set a `z-index` style on the currently dragged item so it appears above the surrounding items.

However, `z-index` only affects items with `position !== "static"`. So to enable this effect ensure the position of the `Reorder.Item` is set to `relative` or `absolute`.

## [API](#api)

### [`Reorder.Group`](#reorder.group)

#### [`as`](#as)

**Default**: `"ul"`

The underlying element for `Reorder.Group` to render as.

```
<Reorder.Group as="div"></Reorder.Group>
```

#### [`axis`](#axis)

**Default**: `"y"`

The direction of reorder detection.

By default, all `Reorder.Item` components will visibly move only on this axis. To allow visual motion (but **not** reordering) on both axes, pass the `drag` prop to child `Reorder.Item` components.

#### [`values`](#values)

The values array that will be reordered. Each item in this list must match a `value` passed to each `Reorder.Item`.

#### [`onReorder`](#onreorder)

A callback that will fire when items are detected to have reordered. The provided `newOrder` should be passed to a `values` state update function.

```
const [items, setItems] = useState([0, 1, 2, 3])

return (
  <Reorder.Group values={items} onReorder={setItems}>
```

### [`Reorder.Item`](#reorder.item)

`Reorder.Item` components accept all `motion` [component props](./react-motion-component) in addition to the following:

#### [`as`](#as-1)

**Default:** `"li"`

The element for `Reorder.Item` to render as.

#### [`value`](#value)

When `onReorder` is called, this is the value that will be passed through in the newly ordered array.

## Related topics

- [### Layout animation

  Smoothly animate layout changes and create shared element animations.](./react-layout-animations)

  [### Layout animation

  Smoothly animate layout changes and create shared element animations.](./react-layout-animations)

  [### Layout animation

  Smoothly animate layout changes and create shared element animations.](./react-layout-animations)
- [### AnimatePresence

  Add exit animations to React components when they're removed from the page.](./react-animate-presence)

  [### AnimatePresence

  Add exit animations to React components when they're removed from the page.](./react-animate-presence)

  [### AnimatePresence

  Add exit animations to React components when they're removed from the page.](./react-animate-presence)

Previous

[MotionConfig](./react-motion-config)

Next

[AnimateNumber](./react-animate-number)

Motion+

Motion+

Motion+

## Level up your animations with Motion+

Unlock the full vault of 330+ Motion examples, 100+ tutorials, premium APIs, private Discord and GitHub, and powerful Motion Studio animation editing tools for your IDE.

[Get Motion+](../plus)

[Get Motion+](../plus)

[Get Motion+](../plus)

One-time payment, lifetime updates.

[![](https://framerusercontent.com/images/5efyyhcUoAlTBRRovqyx3jnMnEM.png?width=1568&height=1174)](https://framerusercontent.com/assets/MK7ot7xHs8BI3SZScC9oiKpURY4.mp4)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

![](https://framerusercontent.com/images/dvcUQX74Mh8wmjKmhIoM2Yli4.png?width=2000&height=2000)

[![](https://framerusercontent.com/images/a6LWvnzoehr1qy4ywp7QSBDq5iQ.jpg?width=290&height=223)

AI-ready animations

Make your LLM an animation expert with 330+ pre-built examples available via MCP.](../plus)