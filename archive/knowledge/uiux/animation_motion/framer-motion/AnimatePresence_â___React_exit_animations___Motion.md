# AnimatePresence â React exit animations | Motion

Source: https://www.framer.com/motion/animate-presence/

---

`AnimatePresence` makes exit animations easy. By wrapping one or more `motion` [components](./react-motion-component) with `AnimatePresence`, we gain access to the `exit` animation prop.

```
<AnimatePresence>
  {show && <motion.div key="modal" exit={{ opacity: 0 }} />}
</AnimatePresence>
```

## [Usage](#usage)

### [Import](#import)

```
import { AnimatePresence } from "motion/react"
```

### [Exit animations](#exit-animations)

`AnimatePresence` works by detecting when its **direct children** are removed from the React tree.

This can be due to a component mounting/remounting:

```
<AnimatePresence>
  {show && <Modal key="modal" />}
</AnimatePresence>
```

Its `key` changing:

```
<AnimatePresence>
  <Slide key={activeItem.id} />
</AnimatePresence>
```

Or when children in a list are added/removed:

```
<AnimatePresence>
  {items.map(item => (
    <motion.li key={item.id} exit={{ opacity: 1 }} layout />
  ))}
</AnimatePresence>
```

Any `motion` components within the exiting component will fire animations defined on their `exit` props before the component is removed from the DOM.

```
function Slide({ img, description }) {
  return (
    <motion.div exit={{ opacity: 0 }}>
      <img src={img.src} />
      <motion.p exit={{ y: 10 }}>{description}</motion.p>
    </motion.div>
  )
}
```

Direct children must each have a unique `key` prop so `AnimatePresence` can track their presence in the tree.

Like `initial` and `animate`, `exit` can be defined either as an object of values, or as a variant label.

```
const modalVariants = {
  visible: { opacity: 1, transition: { when: "beforeChildren" } },
  hidden: { opacity: 0, transition: { when: "afterChildren" } }
}

function Modal({ children }) {
  return (
    <motion.div initial="hidden" animate="visible" exit="hidden">
      {children}
    </motion.div>
  )
}
```

### [Changing `key`](#changing-key)

Changing a `key` prop makes React create an entirely new component. So by changing the `key` of a single child of `AnimatePresence`, we can easily make components like slideshows.

```
export const Slideshow = ({ image }) => (
  <AnimatePresence>
    <motion.img
      key={image.src}
      src={image.src}
      initial={{ x: 300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: -300, opacity: 0 }}
    />
  </AnimatePresence>
)
```

### [Access presence state](#access-presence-state)

Any child of `AnimatePresence` can access presence state with the `useIsPresence` hook.

```
import { useIsPresent } from "motion/react"

function Component() {
  const isPresent = useIsPresent()

  return isPresent ? "Here!" : "Exiting..."
}
```

This allows you to change content or styles when a component is no longer rendered.

### [Access presence data](#access-presence-data)

When a component has been removed from the React tree, its props can no longer be updated. We can use `AnimatePresence`'s `custom` prop to pass new data down through the tree, even into exiting components.

```
<AnimatePresence custom={swipeDirection}>
  <Slide key={activeSlideId}>
```

Then later we can extract that using `usePresenceData`.

```
import { AnimatePresence, usePresenceData } from "motion/react"

function Slide() {
  const isPresent = useIsPresent()
  const direction = usePresenceData()

  return (
    <motion.div exit={{ opacity: 0 }}>
      {isPresent ? "Here!" : "Exiting " + direction}
    </motion.div>
  )
}
```

### [Manual usage](#manual-usage)

It's also possible to manually tell `AnimatePresence` when a component is safe to remove with the `usePresence` hook.

This returns both `isPresent` state and a callback, `safeToRemove`, that should be called when you're ready to remove the component from the DOM (for instance after a manual animation or other timeout).

```
import { usePresence } from "motion/react"

function Component() {
  const [isPresent, safeToRemove] = usePresence()

  useEffect(() => {
    // Remove from DOM 1000ms after being removed from React
    !isPresent && setTimeout(safeToRemove, 1000)
  }, [isPresent])

  return <div />
}
```

### [Propagate exit animations](#propagate-exit-animations)

By default, `AnimatePresence` controls the `exit` animations on all of its children, **until** another `AnimatePresence` component is rendered.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence>
        {/*
          * When `show` becomes `false`, exit animations
          * on these children will not fire.
          */}
        {children}
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

By setting an `AnimatePresence` component's `propagate` prop to `true`, when it's removed from another `AnimatePresence` it will fire all of **its** children's exit animations.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence propagate>
        {/*
          * When `show` becomes `false`, exit animations
          * on these children **will** fire.
          */}
        {children}
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

## [Props](#props)

### [`initial`](#initial)

By passing `initial={false}`, `AnimatePresence` will disable any initial animations on children that are present when the component is first rendered.

```
<AnimatePresence initial={false}>
  <Slide key={activeItem.id} />
</AnimatePresence>
```

### [`custom`](#custom)

When a component is removed, there's no longer a chance to update its props (because it's no longer in the React tree). Therefore we can't update its exit animation with the same render that removed the component.

By passing a value through `AnimatePresence`'s `custom` prop, we can use dynamic variants to change the `exit` animation.

```
const variants = {
  hidden: (direction) => ({
    opacity: 0,
    x: direction === 1 ? -300 : 300
  }),
  visible: { opacity: 1, x: 0 }
}

export const Slideshow = ({ image, direction }) => (
  <AnimatePresence custom={direction}>
    <motion.img
      key={image.src}
      src={image.src}
      variants={variants}
      initial="hidden"
      animate="visible"
      exit="hidden"
    />
  </AnimatePresence>
)
```

This data can be accessed by children via `usePresenceData`.

### [`mode`](#mode)

**Default:** `"sync"`

Decides how `AnimatePresence` handles entering and exiting children.

#### [`sync`](#sync)

In `"sync"` mode, elements animate in and out as soon as they're added/removed.

This is the most basic (and default) mode - `AnimatePresence` takes no opinion on sequencing animations or layout. Therefore, if element layouts conflict (as in the above example), you can either implement your own solution (using `position: absolute` or similar), or try one of the other two `mode` options.

#### [`wait`](#wait)

In `"wait"` mode, the entering element will **wait** until the exiting child has animated out, before it animates in.

This is great for sequential animations, presenting users with one piece of information or one UI element at a time.

`wait` mode only supports one child at a time.

Try setting `ease: "easeIn"` (or similar) on the exit animation, and `ease: "easeOut"` on the enter animation for an overall `easeInOut` easing effect.

#### [`popLayout`](#poplayout)

Exiting elements will be "popped" out of the page layout, allowing surrounding elements to immediately reflow. Pairs especially well with the `layout` prop, so elements can animate to their new layout.

```
<AnimatePresence>
  {items.map(item => (
    <motion.li layout exit={{ opacity: 0 }} />
  )}
</AnimatePresence>
```

When using `popLayout` mode, any immediate child of AnimatePresence that's a custom component **must** be wrapped in React's `forwardRef` function, forwarding the provided `ref` to the DOM node you wish to pop out of the layout.

For a more detailed comparison, check out the [full AnimatePresence modes tutorial](../tutorials/react-animate-presence-modes).

### [`onExitComplete`](#onexitcomplete)

Fires when all exiting nodes have completed animating out.

### [`propagate`](#propagate)

**Default:** `false`

If set to `true`, exit animations on children will also trigger when this `AnimatePresence` exits from a parent `AnimatePresence`.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence propagate>
        {/* This exit prop will now fire when show is false */}
        <motion.div exit={{ x: -100 }} />
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

### [`root`](#root)

Root element for injecting `popLayout` styles. Defaults to `document.head` but can be set to another `ShadowRoot`, for use within shadow DOM.

## [Troubleshooting](#troubleshooting)

### [Exit animations aren't working](#exit-animations-aren-t-working)

Ensure all **immediate** children get a unique `key` prop that **remains the same for that component every render**.

For instance, providing `index` as a `key` is **bad** because if the items reorder then the `index` will not be matched to the `item`:

```
<AnimatePresence>
  {items.map((item, index) => (
    <Component key={index} />
  ))}
</AnimatePresence>
```

It's preferred to pass something that's unique to that item, for instance an ID:

```
<AnimatePresence>
  {items.map((item) => (
    <Component key={item.id} />
  ))}
</AnimatePresence>
```

Also make sure `AnimatePresence` is **outside** of the code that unmounts the element. If `AnimatePresence` itself unmounts, then it can't control exit animations!

For example, this will **not work**:

```
isVisible && (
  <AnimatePresence>
    <Component />
  </AnimatePresence>
)
```

Instead, the conditional should be at the root of `AnimatePresence`:

```
<AnimatePresence>
  {isVisible && <Component />}
</AnimatePresence>
```

### [Layout animations not working with `mode="sync"`](#layout-animations-not-working-with-mode-sync)

When mixing exit and [layout animations](./react-layout-animations), it might be necessary to wrap the group in `LayoutGroup` to ensure that components outside of `AnimatePresence` know when to perform a layout animation.

```
<LayoutGroup>
  <motion.ul layout>
    <AnimatePresence>
      {items.map(item => (
        <motion.li layout key={item.id} />
      ))}
    </AnimatePresence>
  </motion.ul>
</LayoutGroup>
```

### [Layout animations not working with `mode="popLayout"`](#layout-animations-not-working-with-mode-poplayout)

When any HTML element has an active `transform` it temporarily becomes the [offset parent](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetParent) of its children. This can cause children with `position: "absolute"` not to appear where you expect.  
  
`mode="popLayout"` works by using `position: "absolute"`. So to ensure consistent and expected positioning during a layout animation, ensure that the animating parent has a `position` other than `"static"`.

```
<motion.ul layout style={{ position: "relative" }}>
  <AnimatePresence mode="popLayout">
    {items.map(item => (
      <motion.li layout key={item.id} />
    ))}
  </AnimatePresence>
</motion.ul>
```

`AnimatePresence` makes exit animations easy. By wrapping one or more `motion` [components](./react-motion-component) with `AnimatePresence`, we gain access to the `exit` animation prop.

```
<AnimatePresence>
  {show && <motion.div key="modal" exit={{ opacity: 0 }} />}
</AnimatePresence>
```

## [Usage](#usage)

### [Import](#import)

```
import { AnimatePresence } from "motion/react"
```

### [Exit animations](#exit-animations)

`AnimatePresence` works by detecting when its **direct children** are removed from the React tree.

This can be due to a component mounting/remounting:

```
<AnimatePresence>
  {show && <Modal key="modal" />}
</AnimatePresence>
```

Its `key` changing:

```
<AnimatePresence>
  <Slide key={activeItem.id} />
</AnimatePresence>
```

Or when children in a list are added/removed:

```
<AnimatePresence>
  {items.map(item => (
    <motion.li key={item.id} exit={{ opacity: 1 }} layout />
  ))}
</AnimatePresence>
```

Any `motion` components within the exiting component will fire animations defined on their `exit` props before the component is removed from the DOM.

```
function Slide({ img, description }) {
  return (
    <motion.div exit={{ opacity: 0 }}>
      <img src={img.src} />
      <motion.p exit={{ y: 10 }}>{description}</motion.p>
    </motion.div>
  )
}
```

Direct children must each have a unique `key` prop so `AnimatePresence` can track their presence in the tree.

Like `initial` and `animate`, `exit` can be defined either as an object of values, or as a variant label.

```
const modalVariants = {
  visible: { opacity: 1, transition: { when: "beforeChildren" } },
  hidden: { opacity: 0, transition: { when: "afterChildren" } }
}

function Modal({ children }) {
  return (
    <motion.div initial="hidden" animate="visible" exit="hidden">
      {children}
    </motion.div>
  )
}
```

### [Changing `key`](#changing-key)

Changing a `key` prop makes React create an entirely new component. So by changing the `key` of a single child of `AnimatePresence`, we can easily make components like slideshows.

```
export const Slideshow = ({ image }) => (
  <AnimatePresence>
    <motion.img
      key={image.src}
      src={image.src}
      initial={{ x: 300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: -300, opacity: 0 }}
    />
  </AnimatePresence>
)
```

### [Access presence state](#access-presence-state)

Any child of `AnimatePresence` can access presence state with the `useIsPresence` hook.

```
import { useIsPresent } from "motion/react"

function Component() {
  const isPresent = useIsPresent()

  return isPresent ? "Here!" : "Exiting..."
}
```

This allows you to change content or styles when a component is no longer rendered.

### [Access presence data](#access-presence-data)

When a component has been removed from the React tree, its props can no longer be updated. We can use `AnimatePresence`'s `custom` prop to pass new data down through the tree, even into exiting components.

```
<AnimatePresence custom={swipeDirection}>
  <Slide key={activeSlideId}>
```

Then later we can extract that using `usePresenceData`.

```
import { AnimatePresence, usePresenceData } from "motion/react"

function Slide() {
  const isPresent = useIsPresent()
  const direction = usePresenceData()

  return (
    <motion.div exit={{ opacity: 0 }}>
      {isPresent ? "Here!" : "Exiting " + direction}
    </motion.div>
  )
}
```

### [Manual usage](#manual-usage)

It's also possible to manually tell `AnimatePresence` when a component is safe to remove with the `usePresence` hook.

This returns both `isPresent` state and a callback, `safeToRemove`, that should be called when you're ready to remove the component from the DOM (for instance after a manual animation or other timeout).

```
import { usePresence } from "motion/react"

function Component() {
  const [isPresent, safeToRemove] = usePresence()

  useEffect(() => {
    // Remove from DOM 1000ms after being removed from React
    !isPresent && setTimeout(safeToRemove, 1000)
  }, [isPresent])

  return <div />
}
```

### [Propagate exit animations](#propagate-exit-animations)

By default, `AnimatePresence` controls the `exit` animations on all of its children, **until** another `AnimatePresence` component is rendered.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence>
        {/*
          * When `show` becomes `false`, exit animations
          * on these children will not fire.
          */}
        {children}
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

By setting an `AnimatePresence` component's `propagate` prop to `true`, when it's removed from another `AnimatePresence` it will fire all of **its** children's exit animations.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence propagate>
        {/*
          * When `show` becomes `false`, exit animations
          * on these children **will** fire.
          */}
        {children}
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

## [Props](#props)

### [`initial`](#initial)

By passing `initial={false}`, `AnimatePresence` will disable any initial animations on children that are present when the component is first rendered.

```
<AnimatePresence initial={false}>
  <Slide key={activeItem.id} />
</AnimatePresence>
```

### [`custom`](#custom)

When a component is removed, there's no longer a chance to update its props (because it's no longer in the React tree). Therefore we can't update its exit animation with the same render that removed the component.

By passing a value through `AnimatePresence`'s `custom` prop, we can use dynamic variants to change the `exit` animation.

```
const variants = {
  hidden: (direction) => ({
    opacity: 0,
    x: direction === 1 ? -300 : 300
  }),
  visible: { opacity: 1, x: 0 }
}

export const Slideshow = ({ image, direction }) => (
  <AnimatePresence custom={direction}>
    <motion.img
      key={image.src}
      src={image.src}
      variants={variants}
      initial="hidden"
      animate="visible"
      exit="hidden"
    />
  </AnimatePresence>
)
```

This data can be accessed by children via `usePresenceData`.

### [`mode`](#mode)

**Default:** `"sync"`

Decides how `AnimatePresence` handles entering and exiting children.

#### [`sync`](#sync)

In `"sync"` mode, elements animate in and out as soon as they're added/removed.

This is the most basic (and default) mode - `AnimatePresence` takes no opinion on sequencing animations or layout. Therefore, if element layouts conflict (as in the above example), you can either implement your own solution (using `position: absolute` or similar), or try one of the other two `mode` options.

#### [`wait`](#wait)

In `"wait"` mode, the entering element will **wait** until the exiting child has animated out, before it animates in.

This is great for sequential animations, presenting users with one piece of information or one UI element at a time.

`wait` mode only supports one child at a time.

Try setting `ease: "easeIn"` (or similar) on the exit animation, and `ease: "easeOut"` on the enter animation for an overall `easeInOut` easing effect.

#### [`popLayout`](#poplayout)

Exiting elements will be "popped" out of the page layout, allowing surrounding elements to immediately reflow. Pairs especially well with the `layout` prop, so elements can animate to their new layout.

```
<AnimatePresence>
  {items.map(item => (
    <motion.li layout exit={{ opacity: 0 }} />
  )}
</AnimatePresence>
```

When using `popLayout` mode, any immediate child of AnimatePresence that's a custom component **must** be wrapped in React's `forwardRef` function, forwarding the provided `ref` to the DOM node you wish to pop out of the layout.

For a more detailed comparison, check out the [full AnimatePresence modes tutorial](../tutorials/react-animate-presence-modes).

### [`onExitComplete`](#onexitcomplete)

Fires when all exiting nodes have completed animating out.

### [`propagate`](#propagate)

**Default:** `false`

If set to `true`, exit animations on children will also trigger when this `AnimatePresence` exits from a parent `AnimatePresence`.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence propagate>
        {/* This exit prop will now fire when show is false */}
        <motion.div exit={{ x: -100 }} />
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

### [`root`](#root)

Root element for injecting `popLayout` styles. Defaults to `document.head` but can be set to another `ShadowRoot`, for use within shadow DOM.

## [Troubleshooting](#troubleshooting)

### [Exit animations aren't working](#exit-animations-aren-t-working)

Ensure all **immediate** children get a unique `key` prop that **remains the same for that component every render**.

For instance, providing `index` as a `key` is **bad** because if the items reorder then the `index` will not be matched to the `item`:

```
<AnimatePresence>
  {items.map((item, index) => (
    <Component key={index} />
  ))}
</AnimatePresence>
```

It's preferred to pass something that's unique to that item, for instance an ID:

```
<AnimatePresence>
  {items.map((item) => (
    <Component key={item.id} />
  ))}
</AnimatePresence>
```

Also make sure `AnimatePresence` is **outside** of the code that unmounts the element. If `AnimatePresence` itself unmounts, then it can't control exit animations!

For example, this will **not work**:

```
isVisible && (
  <AnimatePresence>
    <Component />
  </AnimatePresence>
)
```

Instead, the conditional should be at the root of `AnimatePresence`:

```
<AnimatePresence>
  {isVisible && <Component />}
</AnimatePresence>
```

### [Layout animations not working with `mode="sync"`](#layout-animations-not-working-with-mode-sync)

When mixing exit and [layout animations](./react-layout-animations), it might be necessary to wrap the group in `LayoutGroup` to ensure that components outside of `AnimatePresence` know when to perform a layout animation.

```
<LayoutGroup>
  <motion.ul layout>
    <AnimatePresence>
      {items.map(item => (
        <motion.li layout key={item.id} />
      ))}
    </AnimatePresence>
  </motion.ul>
</LayoutGroup>
```

### [Layout animations not working with `mode="popLayout"`](#layout-animations-not-working-with-mode-poplayout)

When any HTML element has an active `transform` it temporarily becomes the [offset parent](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetParent) of its children. This can cause children with `position: "absolute"` not to appear where you expect.  
  
`mode="popLayout"` works by using `position: "absolute"`. So to ensure consistent and expected positioning during a layout animation, ensure that the animating parent has a `position` other than `"static"`.

```
<motion.ul layout style={{ position: "relative" }}>
  <AnimatePresence mode="popLayout">
    {items.map(item => (
      <motion.li layout key={item.id} />
    ))}
  </AnimatePresence>
</motion.ul>
```

`AnimatePresence` makes exit animations easy. By wrapping one or more `motion` [components](./react-motion-component) with `AnimatePresence`, we gain access to the `exit` animation prop.

```
<AnimatePresence>
  {show && <motion.div key="modal" exit={{ opacity: 0 }} />}
</AnimatePresence>
```

## [Usage](#usage)

### [Import](#import)

```
import { AnimatePresence } from "motion/react"
```

### [Exit animations](#exit-animations)

`AnimatePresence` works by detecting when its **direct children** are removed from the React tree.

This can be due to a component mounting/remounting:

```
<AnimatePresence>
  {show && <Modal key="modal" />}
</AnimatePresence>
```

Its `key` changing:

```
<AnimatePresence>
  <Slide key={activeItem.id} />
</AnimatePresence>
```

Or when children in a list are added/removed:

```
<AnimatePresence>
  {items.map(item => (
    <motion.li key={item.id} exit={{ opacity: 1 }} layout />
  ))}
</AnimatePresence>
```

Any `motion` components within the exiting component will fire animations defined on their `exit` props before the component is removed from the DOM.

```
function Slide({ img, description }) {
  return (
    <motion.div exit={{ opacity: 0 }}>
      <img src={img.src} />
      <motion.p exit={{ y: 10 }}>{description}</motion.p>
    </motion.div>
  )
}
```

Direct children must each have a unique `key` prop so `AnimatePresence` can track their presence in the tree.

Like `initial` and `animate`, `exit` can be defined either as an object of values, or as a variant label.

```
const modalVariants = {
  visible: { opacity: 1, transition: { when: "beforeChildren" } },
  hidden: { opacity: 0, transition: { when: "afterChildren" } }
}

function Modal({ children }) {
  return (
    <motion.div initial="hidden" animate="visible" exit="hidden">
      {children}
    </motion.div>
  )
}
```

### [Changing `key`](#changing-key)

Changing a `key` prop makes React create an entirely new component. So by changing the `key` of a single child of `AnimatePresence`, we can easily make components like slideshows.

```
export const Slideshow = ({ image }) => (
  <AnimatePresence>
    <motion.img
      key={image.src}
      src={image.src}
      initial={{ x: 300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: -300, opacity: 0 }}
    />
  </AnimatePresence>
)
```

### [Access presence state](#access-presence-state)

Any child of `AnimatePresence` can access presence state with the `useIsPresence` hook.

```
import { useIsPresent } from "motion/react"

function Component() {
  const isPresent = useIsPresent()

  return isPresent ? "Here!" : "Exiting..."
}
```

This allows you to change content or styles when a component is no longer rendered.

### [Access presence data](#access-presence-data)

When a component has been removed from the React tree, its props can no longer be updated. We can use `AnimatePresence`'s `custom` prop to pass new data down through the tree, even into exiting components.

```
<AnimatePresence custom={swipeDirection}>
  <Slide key={activeSlideId}>
```

Then later we can extract that using `usePresenceData`.

```
import { AnimatePresence, usePresenceData } from "motion/react"

function Slide() {
  const isPresent = useIsPresent()
  const direction = usePresenceData()

  return (
    <motion.div exit={{ opacity: 0 }}>
      {isPresent ? "Here!" : "Exiting " + direction}
    </motion.div>
  )
}
```

### [Manual usage](#manual-usage)

It's also possible to manually tell `AnimatePresence` when a component is safe to remove with the `usePresence` hook.

This returns both `isPresent` state and a callback, `safeToRemove`, that should be called when you're ready to remove the component from the DOM (for instance after a manual animation or other timeout).

```
import { usePresence } from "motion/react"

function Component() {
  const [isPresent, safeToRemove] = usePresence()

  useEffect(() => {
    // Remove from DOM 1000ms after being removed from React
    !isPresent && setTimeout(safeToRemove, 1000)
  }, [isPresent])

  return <div />
}
```

### [Propagate exit animations](#propagate-exit-animations)

By default, `AnimatePresence` controls the `exit` animations on all of its children, **until** another `AnimatePresence` component is rendered.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence>
        {/*
          * When `show` becomes `false`, exit animations
          * on these children will not fire.
          */}
        {children}
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

By setting an `AnimatePresence` component's `propagate` prop to `true`, when it's removed from another `AnimatePresence` it will fire all of **its** children's exit animations.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence propagate>
        {/*
          * When `show` becomes `false`, exit animations
          * on these children **will** fire.
          */}
        {children}
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

## [Props](#props)

### [`initial`](#initial)

By passing `initial={false}`, `AnimatePresence` will disable any initial animations on children that are present when the component is first rendered.

```
<AnimatePresence initial={false}>
  <Slide key={activeItem.id} />
</AnimatePresence>
```

### [`custom`](#custom)

When a component is removed, there's no longer a chance to update its props (because it's no longer in the React tree). Therefore we can't update its exit animation with the same render that removed the component.

By passing a value through `AnimatePresence`'s `custom` prop, we can use dynamic variants to change the `exit` animation.

```
const variants = {
  hidden: (direction) => ({
    opacity: 0,
    x: direction === 1 ? -300 : 300
  }),
  visible: { opacity: 1, x: 0 }
}

export const Slideshow = ({ image, direction }) => (
  <AnimatePresence custom={direction}>
    <motion.img
      key={image.src}
      src={image.src}
      variants={variants}
      initial="hidden"
      animate="visible"
      exit="hidden"
    />
  </AnimatePresence>
)
```

This data can be accessed by children via `usePresenceData`.

### [`mode`](#mode)

**Default:** `"sync"`

Decides how `AnimatePresence` handles entering and exiting children.

#### [`sync`](#sync)

In `"sync"` mode, elements animate in and out as soon as they're added/removed.

This is the most basic (and default) mode - `AnimatePresence` takes no opinion on sequencing animations or layout. Therefore, if element layouts conflict (as in the above example), you can either implement your own solution (using `position: absolute` or similar), or try one of the other two `mode` options.

#### [`wait`](#wait)

In `"wait"` mode, the entering element will **wait** until the exiting child has animated out, before it animates in.

This is great for sequential animations, presenting users with one piece of information or one UI element at a time.

`wait` mode only supports one child at a time.

Try setting `ease: "easeIn"` (or similar) on the exit animation, and `ease: "easeOut"` on the enter animation for an overall `easeInOut` easing effect.

#### [`popLayout`](#poplayout)

Exiting elements will be "popped" out of the page layout, allowing surrounding elements to immediately reflow. Pairs especially well with the `layout` prop, so elements can animate to their new layout.

```
<AnimatePresence>
  {items.map(item => (
    <motion.li layout exit={{ opacity: 0 }} />
  )}
</AnimatePresence>
```

When using `popLayout` mode, any immediate child of AnimatePresence that's a custom component **must** be wrapped in React's `forwardRef` function, forwarding the provided `ref` to the DOM node you wish to pop out of the layout.

For a more detailed comparison, check out the [full AnimatePresence modes tutorial](../tutorials/react-animate-presence-modes).

### [`onExitComplete`](#onexitcomplete)

Fires when all exiting nodes have completed animating out.

### [`propagate`](#propagate)

**Default:** `false`

If set to `true`, exit animations on children will also trigger when this `AnimatePresence` exits from a parent `AnimatePresence`.

```
<AnimatePresence>
  {show ? (
    <motion.section exit={{ opacity: 0 }}>
      <AnimatePresence propagate>
        {/* This exit prop will now fire when show is false */}
        <motion.div exit={{ x: -100 }} />
      </AnimatePresence>
    </motion.section>
  ) : null}
</AnimatePresence>
```

### [`root`](#root)

Root element for injecting `popLayout` styles. Defaults to `document.head` but can be set to another `ShadowRoot`, for use within shadow DOM.

## [Troubleshooting](#troubleshooting)

### [Exit animations aren't working](#exit-animations-aren-t-working)

Ensure all **immediate** children get a unique `key` prop that **remains the same for that component every render**.

For instance, providing `index` as a `key` is **bad** because if the items reorder then the `index` will not be matched to the `item`:

```
<AnimatePresence>
  {items.map((item, index) => (
    <Component key={index} />
  ))}
</AnimatePresence>
```

It's preferred to pass something that's unique to that item, for instance an ID:

```
<AnimatePresence>
  {items.map((item) => (
    <Component key={item.id} />
  ))}
</AnimatePresence>
```

Also make sure `AnimatePresence` is **outside** of the code that unmounts the element. If `AnimatePresence` itself unmounts, then it can't control exit animations!

For example, this will **not work**:

```
isVisible && (
  <AnimatePresence>
    <Component />
  </AnimatePresence>
)
```

Instead, the conditional should be at the root of `AnimatePresence`:

```
<AnimatePresence>
  {isVisible && <Component />}
</AnimatePresence>
```

### [Layout animations not working with `mode="sync"`](#layout-animations-not-working-with-mode-sync)

When mixing exit and [layout animations](./react-layout-animations), it might be necessary to wrap the group in `LayoutGroup` to ensure that components outside of `AnimatePresence` know when to perform a layout animation.

```
<LayoutGroup>
  <motion.ul layout>
    <AnimatePresence>
      {items.map(item => (
        <motion.li layout key={item.id} />
      ))}
    </AnimatePresence>
  </motion.ul>
</LayoutGroup>
```

### [Layout animations not working with `mode="popLayout"`](#layout-animations-not-working-with-mode-poplayout)

When any HTML element has an active `transform` it temporarily becomes the [offset parent](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetParent) of its children. This can cause children with `position: "absolute"` not to appear where you expect.  
  
`mode="popLayout"` works by using `position: "absolute"`. So to ensure consistent and expected positioning during a layout animation, ensure that the animating parent has a `position` other than `"static"`.

```
<motion.ul layout style={{ position: "relative" }}>
  <AnimatePresence mode="popLayout">
    {items.map(item => (
      <motion.li layout key={item.id} />
    ))}
  </AnimatePresence>
</motion.ul>
```

## Related topics

- [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)

  [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)

  [### Motion component

  Animate elements with a declarative API. Supports variants, gestures, and layout animations.](./react-motion-component)
- [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)

  [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)

  [Motion+

  ### Cursor

  Create custom cursor and follow-along effects in React.](./cursor)
- [Motion+

  ### AnimateActivity

  Add powerful enter, exit, and layout animations to components managed by React's <Activity>](./react-animate-activity)

  [Motion+

  ### AnimateActivity

  Add powerful enter, exit, and layout animations to components managed by React's <Activity>](./react-animate-activity)

  [Motion+

  ### AnimateActivity

  Add powerful enter, exit, and layout animations to components managed by React's <Activity>](./react-animate-activity)

- [### AnimatePresence examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=animatepresence)

- [### AnimatePresence examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=animatepresence)

- [### AnimatePresence examples

  See all examples & tutorials, with full copy & paste source code.](https://motion.dev/examples?platform=react&search=animatepresence)

- [Tutorial

  ### Exit animation

  An example of animating an element when it's removed from the DOM using AnimatePresence in Motion for React.](../tutorials/react-exit-animation)

- [Tutorial

  ### Exit animation

  An example of animating an element when it's removed from the DOM using AnimatePresence in Motion for React.](../tutorials/react-exit-animation)

- [Tutorial

  ### Exit animation

  An example of animating an element when it's removed from the DOM using AnimatePresence in Motion for React.](../tutorials/react-exit-animation)

Previous

[AnimateActivity](./react-animate-activity)

Next

[LayoutGroup](./react-layout-group)

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